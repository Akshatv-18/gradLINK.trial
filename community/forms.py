from django import forms
from accounts.models import User
from .models import Post, Comment, Message

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'title', 'content', 'image', 'link_url', 'tags']
        widgets = {
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title (optional)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'What would you like to share?'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'link_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Add a link (optional)'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add tags separated by commas'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...'
            })
        }

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select recipient"
    )
    
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Message subject'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Write your message...'}),
        }
