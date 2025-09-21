from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_feed, name='feed'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('create-post/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('messages/', views.messages_inbox, name='messages_inbox'),
    path('send-message/', views.send_message, name='send_message'),
    path('send-message/<int:user_id>/', views.send_message, name='send_message_to_user'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('my-posts/', views.my_posts, name='my_posts'),
]
