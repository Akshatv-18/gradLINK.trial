from django.db import models
from django.utils import timezone
from accounts.models import User

class EventCategory(models.Model):
    """Event categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Event Categories"

    def __str__(self):
        return self.name

class Event(models.Model):
    """Events and meetups model"""
    
    EVENT_TYPES = (
        ('networking', 'Networking'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('conference', 'Conference'),
        ('social', 'Social'),
        ('career_fair', 'Career Fair'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    is_virtual = models.BooleanField(default=False)
    virtual_link = models.URLField(blank=True, help_text="Virtual meeting link")
    max_attendees = models.IntegerField(blank=True, null=True)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.start_datetime > timezone.now()

    @property
    def attendee_count(self):
        return self.registrations.filter(status='registered').count()

class EventRegistration(models.Model):
    """Event registrations model"""
    
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('cancelled', 'Cancelled'),
    )
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"
