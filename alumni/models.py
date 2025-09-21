from django.db import models
from django.utils import timezone
from accounts.models import User

class Connection(models.Model):
    """Model for alumni connections/networking"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text="Optional message with connection request")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"

class MentorshipRequest(models.Model):
    """Model for mentorship requests"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    )
    
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_requests')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_offers')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mentorship: {self.mentee.username} -> {self.mentor.username}"

class AlumniDirectory(models.Model):
    """Model for alumni directory entries"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    allow_contact = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    achievements = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Alumni Directory"

    def __str__(self):
        return f"{self.user.username} - Alumni Directory"
