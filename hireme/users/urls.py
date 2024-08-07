from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('create/', create_user, name='create_user'),
    path('login/', login_view, name='login'),
    path('info/<int:user_id>/', get_user_info, name='get_user_info'),
    path('manage_language/', manage_language, name='add_language'),
    path('<int:user_id>/upload_photo/', upload_photo, name='upload-photo'),
    path('all/', get_all_users, name='get_all_users'),
    path('<int:user_id>/personal_info/', get_user_personal_info, name='user_personal_info'),
    path('<int:user_id>/update_personal_info/', update_user_personal_info, name='update_user_personal_info'),
    path('<int:user_id>/education/', get_user_education_level, name='get_user_education_level'),
    path('<int:user_id>/languages/', get_user_languages, name='get_user_languages'),
    path('<int:user_id>/image/', get_user_image, name='get_user_image'),
    path('<int:user_id>/credentials/', get_user_credentials, name='get_user_credentials'),
    path('<int:user_id>/update_credentials/', update_user_credentials, name='update_user_credentials'),
    path('delete_language/', delete_language, name='delete_language'),
    path('<int:user_id>/delete_photo/', delete_photo, name='delete_photo'),
    path('<int:user_id>/display_links/', display_user_social_links, name='display_user_social_links'),
    path('<int:user_id>/update_links/', update_social_media_links, name='update_social_media_links'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)