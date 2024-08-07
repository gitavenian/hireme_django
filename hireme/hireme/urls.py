
from django.contrib import admin
from .views import *
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('company/', include('company.urls')),
    path('job/', include('job.urls')),
    path('skill/' , include('skills.urls')),
    path('logout/', logout_view, name='logout'),
    path('job/rank_users/<int:job_announcement_id>/', rank_users, name='rank_users'),
    path('job/rank_applied_users/<int:job_announcement_id>/', rank_applied_users, name='rank_applied_users'),
    path('job/rank_applied_users_in_same_city/<int:job_announcement_id>/', rank_applied_users_in_same_city, name='rank_applied_users_in_same_city'),
    path('job/rank_users_in_same_city/<int:job_announcement_id>/', rank_users_in_same_city, name='rank_users_in_same_city'),
    path('users/<int:user_id>/suitable_jobs/', suitable_job_announcements, name='suitable_job_announcements'),
]
