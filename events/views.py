from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Event, EventCategory, EventRegistration
from .forms import EventForm

def event_list_view(request):
    """Events listing with search and filtering"""
    events = Event.objects.filter(is_active=True).select_related('category', 'organizer').order_by('start_datetime')
    
    # Filter by upcoming/past
    time_filter = request.GET.get('time', 'upcoming')
    if time_filter == 'upcoming':
        events = events.filter(start_datetime__gt=timezone.now())
    elif time_filter == 'past':
        events = events.filter(start_datetime__lt=timezone.now())
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
    
    # Filter by event type
    event_type = request.GET.get('event_type')
    if event_type:
        events = events.filter(event_type=event_type)
    
    # Filter by virtual/in-person
    is_virtual = request.GET.get('is_virtual')
    if is_virtual == 'true':
        events = events.filter(is_virtual=True)
    elif is_virtual == 'false':
        events = events.filter(is_virtual=False)
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    categories = EventCategory.objects.all().order_by('name')
    event_types = Event.EVENT_TYPES
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'categories': categories,
        'event_types': event_types,
        'selected_category': category_id,
        'selected_event_type': event_type,
        'selected_time_filter': time_filter,
        'selected_virtual_filter': is_virtual,
    }
    return render(request, 'events/event_list.html', context)

def event_detail_view(request, event_id):
    """Event detail page"""
    event = get_object_or_404(Event, id=event_id, is_active=True)
    
    # Check if user is registered
    is_registered = False
    registration = None
    is_organizer = False
    if request.user.is_authenticated:
        is_organizer = event.organizer == request.user
        try:
            registration = EventRegistration.objects.get(event=event, user=request.user)
            is_registered = True
        except EventRegistration.DoesNotExist:
            pass
    
    context = {
        'event': event,
        'is_registered': is_registered,
        'registration': registration,
        'is_organizer': is_organizer,  # Pass organizer status to template
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def register_for_event(request, event_id):
    """Register for an event"""
    event = get_object_or_404(Event, id=event_id, is_active=True)
    
    if event.organizer == request.user:
        messages.error(request, 'Event organizers cannot register for their own events.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Check if registration is still open
    if event.registration_deadline and timezone.now() > event.registration_deadline:
        messages.error(request, 'Registration for this event has closed.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Check if event is full
    if event.max_attendees and event.attendee_count >= event.max_attendees:
        messages.error(request, 'This event is full.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Check if user is already registered
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, 'You are already registered for this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Create registration
    EventRegistration.objects.create(event=event, user=request.user)
    messages.success(request, 'You have successfully registered for this event!')
    return redirect('events:event_detail', event_id=event.id)

@login_required
def unregister_from_event(request, event_id):
    """Unregister from an event"""
    event = get_object_or_404(Event, id=event_id, is_active=True)
    
    try:
        registration = EventRegistration.objects.get(event=event, user=request.user)
        registration.delete()
        messages.success(request, 'You have successfully unregistered from this event.')
    except EventRegistration.DoesNotExist:
        messages.error(request, 'You are not registered for this event.')
    
    return redirect('events:event_detail', event_id=event.id)

@login_required
def create_event(request):
    """Create a new event"""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()
    
    context = {
        'form': form,
    }
    return render(request, 'events/create_event.html', context)

@login_required
def edit_event(request, event_id):
    """Edit an existing event"""
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'is_edit': True,
    }
    return render(request, 'events/edit_event.html', context)

@login_required
def delete_event(request, event_id):
    """Delete an event"""
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Event "{event_title}" has been deleted successfully.')
        return redirect('events:my_events')
    
    context = {
        'event': event,
    }
    return render(request, 'events/delete_event.html', context)

@login_required
def my_events(request):
    """View user's events (organized and registered)"""
    # Events organized by user
    organized_events = Event.objects.filter(organizer=request.user).order_by('-created_at')
    
    # Events user is registered for
    registered_events = Event.objects.filter(
        registrations__user=request.user,
        registrations__status='registered'
    ).order_by('start_datetime')
    
    context = {
        'organized_events': organized_events,
        'registered_events': registered_events,
    }
    return render(request, 'events/my_events.html', context)
