from django import forms
from .models import Event, EventCategory

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'category', 'start_datetime', 'end_datetime',
                 'location', 'is_virtual', 'virtual_link', 'max_attendees', 'registration_deadline',
                 'is_free', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'start_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'is_virtual': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'virtual_link': forms.URLInput(attrs={'class': 'form-control'}),
            'max_attendees': forms.NumberInput(attrs={'class': 'form-control'}),
            'registration_deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
