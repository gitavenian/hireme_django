from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('create_branch/', create_branch, name='create_branch'),
    path('branch/<int:branch_id>/', get_branch_info, name='get_branch_info'),
    path('branch/update/<int:branch_id>/', update_branch, name='update_branch'),
    path('all_companies/', get_all_companies, name='get_all_companies'),
    path('branches/', get_all_branches, name='get_all_branches'),
    path('branch/<int:branch_id>/announcements/', get_announcements_by_branch, name='announcements_by_branch'),
    path('branch/<int:branch_id>/upload-image/', upload_branch_image, name='upload_branch_image'),
    path('branch/<int:branch_id>/main_page/', filter_users_by_job_nature, name='filter_users'),
    path('skills_by_branch/<int:branch_id>/', get_branch_job_nature, name='skills_by_branch'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
