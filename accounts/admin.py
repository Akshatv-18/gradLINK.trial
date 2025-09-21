from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, University, UserProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_verified', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'profile_picture', 'bio', 'phone', 'location', 
                      'website', 'linkedin_url', 'is_verified')
        }),
    )

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'established_year', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('established_year',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'graduation_year', 'current_position', 'is_mentor')
    list_filter = ('is_mentor', 'is_looking_for_mentor', 'graduation_year')
    search_fields = ('user__username', 'user__email', 'current_company', 'degree')

from django.contrib import admin

admin.site.site_header = "gradLINK ADMIN"
admin.site.site_title = "gradLINK ADMIN"
admin.site.index_title = "Welcome|ADMIN|Dashboard"
