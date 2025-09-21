from django.contrib import admin
from .models import EventCategory, Event, EventRegistration

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at')
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'organizer', 'start_datetime', 'location', 'is_active')
    list_filter = ('event_type', 'is_active', 'is_virtual', 'is_free', 'start_datetime')
    search_fields = ('title', 'description', 'location', 'organizer__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'registered_at')
    list_filter = ('status', 'registered_at')
    search_fields = ('user__username', 'event__title')
