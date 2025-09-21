from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, LoginForm, UserProfileForm, UserUpdateForm, DeleteProfileForm
from .models import User, UserProfile

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('core:dashboard')

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    next_page = 'core:home'
    
    def dispatch(self, request, *args, **kwargs):
        # Handle both GET and POST requests
        return super().dispatch(request, *args, **kwargs)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_view(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': user == request.user,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def dashboard_view(request):
    """User dashboard view"""
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def delete_profile(request):
    if request.method == 'POST':
        form = DeleteProfileForm(user=request.user, data=request.POST)
        if form.is_valid():
            try:
                user = request.user
                user.delete()
                messages.success(request, "Your profile has been deleted successfully.")
                return redirect('core:home')
            except Exception as e:
                messages.error(request, "An error occurred while deleting your profile. Please try again.")
                return redirect('accounts:profile')
        else:
            messages.error(request, "Please enter the correct password to delete your profile.")
            return render(request, 'accounts/delete_profile.html', {'form': form})
    else:
        form = DeleteProfileForm(user=request.user)
    
    return render(request, 'accounts/delete_profile.html', {'form': form})
