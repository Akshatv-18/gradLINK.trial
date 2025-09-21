from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.models import User
from .models import Post, PostLike, Comment, Message
from .forms import PostForm, CommentForm, MessageForm

def community_feed(request):
    """Community feed with posts"""
    posts = Post.objects.filter(is_active=True).select_related('author').prefetch_related('likes', 'comments').order_by('-is_pinned', '-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Filter by post type
    post_type = request.GET.get('post_type')
    if post_type:
        posts = posts.filter(post_type=post_type)
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get post types for filter
    post_types = Post.POST_TYPES
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'post_types': post_types,
        'selected_post_type': post_type,
    }
    return render(request, 'community/feed.html', context)

def post_detail_view(request, post_id):
    """Post detail with comments"""
    post = get_object_or_404(Post, id=post_id, is_active=True)
    comments = Comment.objects.filter(post=post, is_active=True, parent__isnull=True).select_related('author').prefetch_related('replies').order_by('created_at')
    
    # Check if user has liked the post
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = PostLike.objects.filter(post=post, user=request.user).exists()
    
    context = {
        'post': post,
        'comments': comments,
        'user_has_liked': user_has_liked,
    }
    return render(request, 'community/post_detail.html', context)

@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('community:post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'community/create_post.html', context)

@login_required
def like_post(request, post_id):
    """Like/unlike a post (AJAX)"""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': post.like_count
        })
    
    return JsonResponse({'success': False})

@login_required
def add_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id, is_active=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # Handle reply to another comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id, post=post)
                comment.parent = parent_comment
            
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('community:post_detail', post_id=post.id)

@login_required
def messages_inbox(request):
    """User's message inbox"""
    received_messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender').order_by('-created_at')
    
    sent_messages = Message.objects.filter(
        sender=request.user
    ).select_related('receiver').order_by('-created_at')
    
    context = {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    }
    return render(request, 'community/messages.html', context)

@login_required
def send_message(request, user_id=None):
    """Send a message to another user"""
    recipient = None
    if user_id:
        recipient = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if recipient:
                message.receiver = recipient
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('community:messages_inbox')
    else:
        initial_data = {}
        if recipient:
            initial_data['receiver'] = recipient
        form = MessageForm(initial=initial_data)
    
    context = {
        'form': form,
        'recipient': recipient,
    }
    return render(request, 'community/send_message.html', context)

@login_required
def message_detail(request, message_id):
    """View a specific message"""
    message = get_object_or_404(
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)),
        id=message_id
    )
    
    # Mark as read if user is the receiver
    if message.receiver == request.user and not message.is_read:
        message.is_read = True
        message.save()
    
    context = {
        'message': message,
    }
    return render(request, 'community/message_detail.html', context)

@login_required
def my_posts(request):
    """View user's posts"""
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'posts': posts,
    }
    return render(request, 'community/my_posts.html', context)
