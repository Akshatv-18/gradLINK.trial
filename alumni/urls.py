from django.urls import path
from . import views

app_name = 'alumni'

urlpatterns = [
    path('directory/', views.directory_view, name='directory'),
    path('connections/', views.my_connections, name='my_connections'),
    path('connect/<int:user_id>/', views.send_connection_request, name='send_connection'),
    path('respond-connection/<int:connection_id>/', views.respond_to_connection, name='respond_connection'),
    path('mentorship/', views.mentorship_requests, name='mentorship_requests'),
    path('mentors/', views.mentors_view, name='mentors'),
    path('request-mentorship/<int:mentor_id>/', views.send_mentorship_request, name='send_mentorship_request'),
    path('respond-mentorship/<int:request_id>/', views.respond_to_mentorship, name='respond_mentorship'),
]
