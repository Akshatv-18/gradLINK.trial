from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from accounts.models import User, UserProfile, University


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'user_type':
                field.widget.attrs['class'] = 'form-select'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            # If email is provided, find the username
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                pass
        return username

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['university', 'graduation_year', 'degree', 'major', 'current_position', 
                 'current_company', 'industry', 'experience_years', 'skills', 'interests',
                 'is_mentor', 'is_looking_for_mentor', 'is_open_to_networking']
        widgets = {
            'university': forms.Select(attrs={'class': 'form-select'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'current_position': forms.TextInput(attrs={'class': 'form-control'}),
            'current_company': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_mentor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_looking_for_mentor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_open_to_networking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'phone', 'location', 
                 'website', 'linkedin_url', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class DeleteProfileForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password to confirm deletion'
        }),
        label='Confirm Password',
        help_text='Please enter your current password to confirm profile deletion.'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not authenticate(username=self.user.username, password=password):
            raise forms.ValidationError('Incorrect password. Please try again.')
        return password

class ConnectionRequestForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

class MentorshipRequestForm(forms.Form):
    mentee = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
