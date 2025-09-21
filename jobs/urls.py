from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_for_job, name='apply_job'),
    path('post/', views.post_job, name='post_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-posted-jobs/', views.my_posted_jobs, name='my_posted_jobs'),
]
