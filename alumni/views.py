from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.models import User, UserProfile, University
from .models import Connection, MentorshipRequest, AlumniDirectory
from .forms import ConnectionRequestForm, MentorshipRequestForm

def directory_view(request):
    """Alumni directory with search and filtering"""
    users = User.objects.filter(
        user_type__in=['alumni', 'student'],
        is_active=True
    ).select_related('profile').prefetch_related('profile__university')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(profile__current_company__icontains=search_query) |
            Q(profile__current_position__icontains=search_query) |
            Q(profile__skills__icontains=search_query)
        )
    
    # Filter by university
    university_id = request.GET.get('university')
    if university_id:
        users = users.filter(profile__university_id=university_id)
    
    # Filter by graduation year
    graduation_year = request.GET.get('graduation_year')
    if graduation_year:
        users = users.filter(profile__graduation_year=graduation_year)
    
    # Filter by user type
    user_type = request.GET.get('user_type')
    if user_type:
        users = users.filter(user_type=user_type)
    
    # Filter by mentorship availability
    is_mentor = request.GET.get('is_mentor')
    if is_mentor == 'true':
        users = users.filter(profile__is_mentor=True)
    
    # Exclude current user
    if request.user.is_authenticated:
        users = users.exclude(id=request.user.id)
    
    # Pagination
    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    universities = University.objects.all().order_by('name')
    graduation_years = UserProfile.objects.exclude(graduation_year__isnull=True).values_list('graduation_year', flat=True).distinct().order_by('-graduation_year')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'universities': universities,
        'graduation_years': graduation_years,
        'selected_university': university_id,
        'selected_graduation_year': graduation_year,
        'selected_user_type': user_type,
        'is_mentor_filter': is_mentor,
    }
    return render(request, 'alumni/directory.html', context)

@login_required
def send_connection_request(request, user_id):
    """Send connection request to another user"""
    if request.method == 'POST':
        receiver = get_object_or_404(User, id=user_id)
        
        # Check if connection already exists
        existing_connection = Connection.objects.filter(
            Q(sender=request.user, receiver=receiver) |
            Q(sender=receiver, receiver=request.user)
        ).first()
        
        if existing_connection:
            return JsonResponse({'success': False, 'message': 'Connection already exists'})
        
        # Create connection request
        connection = Connection.objects.create(
            sender=request.user,
            receiver=receiver,
            message=request.POST.get('message', '')
        )
        
        return JsonResponse({'success': True, 'message': 'Connection request sent'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def my_connections(request):
    """View user's connections"""
    # Accepted connections
    connections = Connection.objects.filter(
        Q(sender=request.user, status='accepted') |
        Q(receiver=request.user, status='accepted')
    ).select_related('sender', 'receiver')
    
    # Pending requests sent by user
    sent_requests = Connection.objects.filter(
        sender=request.user,
        status='pending'
    ).select_related('receiver')
    
    # Pending requests received by user
    received_requests = Connection.objects.filter(
        receiver=request.user,
        status='pending'
    ).select_related('sender')
    
    context = {
        'connections': connections,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'alumni/connections.html', context)

@login_required
def respond_to_connection(request, connection_id):
    """Accept or decline connection request"""
    if request.method == 'POST':
        connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
        action = request.POST.get('action')
        
        if action == 'accept':
            connection.status = 'accepted'
            connection.save()
            messages.success(request, 'Connection request accepted!')
        elif action == 'decline':
            connection.status = 'declined'
            connection.save()
            messages.info(request, 'Connection request declined.')
        
        return redirect('alumni:my_connections')
    
    return redirect('alumni:my_connections')

@login_required
def mentorship_requests(request):
    """View mentorship requests"""
    # Requests sent by user (as mentee)
    sent_requests = MentorshipRequest.objects.filter(
        mentee=request.user
    ).select_related('mentor').order_by('-created_at')
    
    # Requests received by user (as mentor)
    received_requests = MentorshipRequest.objects.filter(
        mentor=request.user
    ).select_related('mentee').order_by('-created_at')
    
    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'alumni/mentorship.html', context)

@login_required
def send_mentorship_request(request, mentor_id):
    """Send mentorship request"""
    mentor = get_object_or_404(User, id=mentor_id, profile__is_mentor=True)
    
    if request.method == 'POST':
        form = MentorshipRequestForm(request.POST)
        if form.is_valid():
            mentorship_request = form.save(commit=False)
            mentorship_request.mentee = request.user
            mentorship_request.mentor = mentor
            mentorship_request.save()
            messages.success(request, 'Mentorship request sent successfully!')
            return redirect('alumni:directory')
    else:
        form = MentorshipRequestForm()
    
    context = {
        'form': form,
        'mentor': mentor,
    }
    return render(request, 'alumni/send_mentorship_request.html', context)

@login_required
def respond_to_mentorship(request, request_id):
    """Respond to mentorship request"""
    if request.method == 'POST':
        mentorship_request = get_object_or_404(MentorshipRequest, id=request_id, mentor=request.user)
        action = request.POST.get('action')
        
        if action == 'accept':
            mentorship_request.status = 'accepted'
            mentorship_request.save()
            messages.success(request, 'Mentorship request accepted!')
        elif action == 'decline':
            mentorship_request.status = 'declined'
            mentorship_request.save()
            messages.info(request, 'Mentorship request declined.')
        
        return redirect('alumni:mentorship_requests')
    
    return redirect('alumni:mentorship_requests')

def mentors_view(request):
    """View available mentors"""
    mentors = User.objects.filter(
        profile__is_mentor=True,
        is_active=True
    ).select_related('profile').prefetch_related('profile__university')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        mentors = mentors.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(profile__current_company__icontains=search_query) |
            Q(profile__current_position__icontains=search_query) |
            Q(profile__skills__icontains=search_query) |
            Q(profile__industry__icontains=search_query)
        )
    
    # Filter by industry
    industry = request.GET.get('industry')
    if industry:
        mentors = mentors.filter(profile__industry__icontains=industry)
    
    # Pagination
    paginator = Paginator(mentors, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get industries for filter
    industries = UserProfile.objects.exclude(industry='').values_list('industry', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'industries': industries,
        'selected_industry': industry,
    }
    return render(request, 'alumni/mentors.html', context)
