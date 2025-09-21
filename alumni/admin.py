from django.contrib import admin
from .models import Connection, MentorshipRequest, AlumniDirectory

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'sender__email', 'receiver__email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ('mentee', 'mentor', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('mentee__username', 'mentor__username', 'subject')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AlumniDirectory)
class AlumniDirectoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_public', 'allow_contact', 'featured', 'created_at')
    list_filter = ('is_public', 'allow_contact', 'featured', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
