from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST , require_GET
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.http import JsonResponse
from job.models import JobAnnouncement , AppliedJob
from users.models import User
from company.models import Branch
from .ml_utils import *

@require_GET
def rank_users(request, job_announcement_id):
    job_announcement = get_object_or_404(JobAnnouncement, pk=job_announcement_id)
    users = User.objects.all()
    user_points = []

    for user in users:
        point = get_user_points(job_announcement, user)
        user_points.append((user, point))

    # Sort users by their points in descending order
    user_points.sort(key=lambda x: x[1], reverse=True)

    # Serialize user data based on the sorted order
    user_data = [
        {
            'user_id': user.user_id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'phone_number': user.phone_number,
            'city': user.city,
            'educationLevel': user.educationLevel,
            'gender': user.gender,
            'points': point
        }
        for user, point in user_points
    ]

    response_data = {
        'length': len(user_data),
        'users': user_data
    }

    return JsonResponse(response_data)



@require_GET
def rank_users_in_same_city(request, job_announcement_id):
    job_announcement = get_object_or_404(JobAnnouncement, pk=job_announcement_id)
    branch = job_announcement.branch
    city = branch.city
    users = User.objects.filter(city=city)
    user_points = []

    for user in users:
        point = get_user_points(job_announcement, user)
        user_points.append((user, point))

    # Sort users by their points in descending order
    user_points.sort(key=lambda x: x[1], reverse=True)

    # Serialize user data based on the sorted order
    user_data = [
        {
            'user_id': user.user_id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'phone_number': user.phone_number,
            'city': user.city,
            'educationLevel': user.educationLevel,
            'gender': user.gender,
            'points': point
        }
        for user, point in user_points
    ]

    response_data = {
        'length': len(user_data),
        'users': user_data
    }

    return JsonResponse(response_data)


@csrf_exempt
@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"}, status=200)

@require_GET
def rank_applied_users(request, job_announcement_id):
    job_announcement = get_object_or_404(JobAnnouncement, pk=job_announcement_id)
    applied_jobs = AppliedJob.objects.filter(jobAnnouncement=job_announcement)
    user_points = []

    for applied_job in applied_jobs:
        user = applied_job.user
        point = get_user_points(job_announcement, user)
        user_points.append((user, point))

    # Sort users by their points in descending order
    user_points.sort(key=lambda x: x[1], reverse=True)

    # Serialize user data based on the sorted order
    user_data = [
        {
            'user_id': user.user_id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'phone_number': user.phone_number,
            'city': user.city,
            'educationLevel': user.educationLevel,
            'gender': user.gender,
            'points': point
        }
        for user, point in user_points
    ]

    response_data = {
        'length': len(user_data),
        'users': user_data
    }

    return JsonResponse(response_data)


@require_GET
def rank_applied_users_in_same_city(request, job_announcement_id):
    job_announcement = get_object_or_404(JobAnnouncement, pk=job_announcement_id)
    branch = job_announcement.branch
    city = branch.city
    applied_jobs = AppliedJob.objects.filter(jobAnnouncement=job_announcement)
    user_points = []

    for applied_job in applied_jobs:
        user = applied_job.user
        if user.city == city:
            point = get_user_points(job_announcement, user)
            user_points.append((user, point))

    # Sort users by their points in descending order
    user_points.sort(key=lambda x: x[1], reverse=True)

    # Serialize user data based on the sorted order
    user_data = [
        {
            'user_id': user.user_id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'phone_number': user.phone_number,
            'city': user.city,
            'educationLevel': user.educationLevel,
            'gender': user.gender,
            'points': point
        }
        for user, point in user_points
    ]

    response_data = {
        'length': len(user_data),
        'users': user_data
    }

    return JsonResponse(response_data)

@require_GET
def suitable_job_announcements(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_city = user.city
    job_announcements = JobAnnouncement.objects.filter(branch__city=user_city)

    suitable_jobs = []
    for job_announcement in job_announcements:
        if check_job_suitability(job_announcement, user) == 1:
            user_point = get_user_points(job_announcement, user)
            suitable_jobs.append((job_announcement, user_point))

    # Sort job announcements by user points in descending order and then by creation date in descending order
    suitable_jobs.sort(key=lambda x: (-x[1], -x[0].createdAt.toordinal()))

    # Serialize job announcement data
    job_data = [
        {
            'jobAnnouncement_id': job.jobAnnouncement_id,
            'job_title': job.job_title,
            'branch': job.branch.name,
            'experience': job.experience,
            'city': job.branch.city,
            'createdAt': job.createdAt.strftime('%d-%m-%Y'),  # Formatting the date
            'user_points': points
        }
        for job, points in suitable_jobs
    ]

    response_data = {
        'length': len(job_data),
        'jobs': job_data
    }

    return JsonResponse(response_data)