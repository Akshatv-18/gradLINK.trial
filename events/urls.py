from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list_view, name='event_list'),
    path('<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('<int:event_id>/register/', views.register_for_event, name='register_event'),
    path('create/', views.create_event, name='create_event'),
    path('my-events/', views.my_events, name='my_events'),
    path('register/<int:event_id>/', views.register_for_event, name='register'),
    path('unregister/<int:event_id>/', views.unregister_from_event, name='unregister'),
    path('my-events/', views.my_events, name='my_events'),
    path('<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),
]
