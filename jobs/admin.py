from django.contrib import admin
from .models import JobCategory, Job, JobApplication

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'posted_by', 'is_active', 'created_at')
    list_filter = ('job_type', 'experience_level', 'is_active', 'created_at', 'category')
    search_fields = ('title', 'company', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('applicant__username', 'job__title', 'job__company')
