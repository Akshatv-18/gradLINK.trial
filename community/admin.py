from django.contrib import admin
from .models import Post, PostLike, Comment, Message

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'title', 'is_pinned', 'is_active', 'created_at')
    list_filter = ('post_type', 'is_pinned', 'is_active', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'tags')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author__username', 'content', 'post__title')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'subject', 'content')
