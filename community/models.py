from django.db import models
from django.utils import timezone
from accounts.models import User

class Post(models.Model):
    """Community posts model"""
    
    POST_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('link', 'Link'),
        ('question', 'Question'),
        ('announcement', 'Announcement'),
    )
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='text')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    link_url = models.URLField(blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.title or self.content[:50]}"

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

class PostLike(models.Model):
    """Post likes model"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title or 'post'}"

class Comment(models.Model):
    """Comments model"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

class Message(models.Model):
    """Private messages model"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.subject or 'Message'}"
