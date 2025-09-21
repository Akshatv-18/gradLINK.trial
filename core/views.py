from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from events.models import Event
from community.models import Post
from django.utils import timezone

def home_view(request):
    """Home page view"""
    context = {
        'recent_jobs': Job.objects.filter(is_active=True)[:6],
        'upcoming_events': Event.objects.filter(
            start_datetime__gt=timezone.now(),
            is_active=True
        )[:4],
        'recent_posts': Post.objects.filter(is_active=True)[:5],
    }
    return render(request, 'core/home.html', context)

@login_required
def dashboard_view(request):
    """User dashboard"""
    context = {
        'user': request.user,
        'recent_jobs': Job.objects.filter(is_active=True)[:5],
        'upcoming_events': Event.objects.filter(
            start_datetime__gt=timezone.now(),
            is_active=True
        )[:3],
        'recent_posts': Post.objects.filter(is_active=True)[:4],
    }
    return render(request, 'accounts\dashboard.html', context)
