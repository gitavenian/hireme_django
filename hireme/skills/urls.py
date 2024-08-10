from django.urls import path
from .views import *

urlpatterns = [
    path('add_skill/', add_skill, name='add_skill'),
    path('add_job/', add_previous_job, name='add_previous_job'),
    path('get_skills/<int:user_id>/', get_skills_by_user_id, name='get_skills_by_user_id'),
    path('get_jobs/<int:user_id>/', get_previous_jobs_by_user_id, name='get_previous_jobs_by_user_id'),
    path('filtered_skills/<int:user_id>/', get_user_skills, name='get_previous_jobs_by_user_id'),
]