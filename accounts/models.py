from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    """Extended user model for GRADLINK"""
    
    USER_TYPES = (
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('university', 'University'),
        ('company', 'Company'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class University(models.Model):
    """University model"""
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='university_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    established_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extended profile information for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    degree = models.CharField(max_length=100, blank=True)
    major = models.CharField(max_length=100, blank=True)
    current_position = models.CharField(max_length=100, blank=True)
    current_company = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    experience_years = models.IntegerField(default=0)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    interests = models.TextField(blank=True, help_text="Comma-separated interests")
    is_mentor = models.BooleanField(default=False)
    is_looking_for_mentor = models.BooleanField(default=False)
    is_open_to_networking = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_skills_list(self):
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]

    def get_interests_list(self):
        return [interest.strip() for interest in self.interests.split(',') if interest.strip()]
