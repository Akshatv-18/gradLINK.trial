from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Job, JobCategory, JobApplication
from .forms import JobForm, JobApplicationForm

def job_list_view(request):
    """Job board with search and filtering"""
    jobs = Job.objects.filter(is_active=True).select_related('category', 'posted_by').order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        jobs = jobs.filter(category_id=category_id)
    
    # Filter by job type
    job_type = request.GET.get('job_type')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Filter by experience level
    experience_level = request.GET.get('experience_level')
    if experience_level:
        jobs = jobs.filter(experience_level=experience_level)
    
    # Filter by location
    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    categories = JobCategory.objects.all().order_by('name')
    job_types = Job.JOB_TYPES
    experience_levels = Job.EXPERIENCE_LEVELS
    locations = Job.objects.values_list('location', flat=True).distinct().order_by('location')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'categories': categories,
        'job_types': job_types,
        'experience_levels': experience_levels,
        'locations': locations,
        'selected_category': category_id,
        'selected_job_type': job_type,
        'selected_experience_level': experience_level,
        'selected_location': location,
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail_view(request, job_id):
    """Job detail page"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if user has already applied
    has_applied = False
    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    
    context = {
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def apply_for_job(request, job_id):
    """Apply for a job"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if user has already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', job_id=job.id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = JobApplicationForm()
    
    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'jobs/apply_job.html', context)

@login_required
def post_job(request):
    """Post a new job"""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = JobForm()
    
    context = {
        'form': form,
    }
    return render(request, 'jobs/post_job.html', context)

@login_required
def my_applications(request):
    """View user's job applications"""
    applications = JobApplication.objects.filter(
        applicant=request.user
    ).select_related('job').order_by('-applied_at')
    
    context = {
        'applications': applications,
    }
    return render(request, 'jobs/my_applications.html', context)

@login_required
def my_posted_jobs(request):
    """View jobs posted by user"""
    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    
    context = {
        'jobs': jobs,
    }
    return render(request, 'jobs/my_posted_jobs.html', context)
