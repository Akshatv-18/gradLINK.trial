from django import forms
from .models import Job, JobApplication, JobCategory

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'job_type', 'experience_level', 'category',
                 'description', 'requirements', 'salary_min', 'salary_max', 'application_deadline', 'external_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'experience_level': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'application_deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'external_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write a compelling cover letter explaining why you are the perfect fit for this role...'
            }),
            'resume': forms.FileInput(attrs={'class': 'form-control'})
        }
