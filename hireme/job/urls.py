from django.urls import path
# from .views import create_job_announcement, get_all_job_announcements , get_job_announcement_info ,  apply_for_job , get_applied_jobs_for_announcement_user, get_applied_jobs_for_announcement, get_applied_jobs_for_user
from .views import *
urlpatterns = [
    path('create_job/', create_or_update_job_announcement, name='create_job_announcement'),
    path('all_announcements/', get_all_job_announcements, name='get_all_job_announcements'),
    path('job_announcement/<int:job_id>/', get_job_announcement_info, name='get_job_announcement_info'),
    path('apply_for_job/', apply_for_job, name='apply_for_job'),
    path('applied_jobs/<int:user_id>/<int:appliedJob_id>/delete/', delete_applied_job, name='delete_applied_job'),
    path('applied_jobs/<int:job_announcement_id>/', get_applied_jobs_for_announcement, name='get_applied_jobs_for_announcement'),
    path('applied_jobs/user/<int:user_id>/', get_applied_jobs_for_user, name='get_applied_jobs_for_user'),
    path('applied_jobs/status/', update_or_create_applied_job_status, name='update_or_create_applied_job_status'),
    path('notification/<int:user_id>/', get_latest_notification, name='get_latest_notification'),
    path('job_announcements/<int:job_announcement_id>/toggle_is_available/', toggle_is_available, name='toggle_is_available'),
    path('add_job_nature/', add_job_nature, name='add_job_nature'),
    path('filter/', job_filtered, name='combined_job_search'),
    path('job_natures/', get_all_job_natures, name='all_job_natures'),
    path('branch/job_announcements/<int:branch_id>/', get_branch_job_announcements, name='all_job_natures'),
]

