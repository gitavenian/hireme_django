from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST , require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import os
import random
import json
from company.models import Branch
from .models import JobNature, JobAnnouncement, AppliedJob
from users.models import User
from datetime import datetime, timedelta
from skills.models import Skill
from .models import AppliedJob, JobAnnouncement, Interview

import logging


def get_custom_message(status, first_name, company_name, job_title=None, interview_date=None, interview_time=None, place=None):
    templates = {
        'Waiting': (
            "Dear {name},\n\n"
            "Your application is under review by {company}. Wish you all the best.\n\n"
            "Best regards,\n"
            "{company} Team"
        ),
        'Accepted': (
            "Dear {name},\n\n"
            "Congratulations on being accepted for the position of {job_title} at {company}. "
            "We are excited to welcome you to our team.\n\n"
            "Please await further instructions regarding the next steps in the onboarding process.\n\n"
            "Best regards,\n"
            "{company} Team"
        ),
        'Rejected': (
            "Dear {name},\n\n"
            "Thank you for your interest in the position of {job_title} at {company}. "
            "After careful consideration, we regret to inform you that we have decided not to proceed with your application.\n\n"
            "We appreciate your effort and encourage you to apply for future opportunities that match your skills and experience.\n\n"
            "Best wishes,\n"
            "{company} Team"
        ),
        'To be Interviewed': (
            "Dear {name},\n\n"
            "We are pleased to invite you to an interview for the position of {job_title} at {company}. "
            "Your interview is scheduled on {interview_date} at {interview_time} in {place}.\n\n"
            "Please confirm your availability for the scheduled time.\n\n"
            "Best regards,\n"
            "{company} Team"
        )
    }

    message = templates.get(status, "Status not recognized")

    # Use format with additional parameters for placeholders
    return message.format(
        name=first_name,
        company=company_name,
        job_title=job_title or "",
        interview_date=interview_date or "",
        interview_time=interview_time or "",
        place=place or ""
    )


def get_status_name(status):
    status_names = {
        'Waiting': 'Under Reviewing',
        'Accepted': 'Hired',
        'Rejected': 'Not Selected',
        'To be Interviewed': 'Interview Stage'
    }
    return status_names.get(status, "Unknown Status")


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@csrf_exempt
@require_http_methods(["POST"])
def create_or_update_job_announcement(request):
    try:
        data = json.loads(request.body)

        required_fields = [
            'job_title', 'job_description', 'branch_id', 'jobNature_id', 'gender', 
            'educationLevel', 'type_of_employment', 'experience', 'salary'
        ]

        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        branch = Branch.objects.get(pk=data['branch_id'])
        jobNature = JobNature.objects.get(pk=data['jobNature_id'])

        job_announcement_id = data.get('job_announcement_id')

        if job_announcement_id:
            job_announcement = JobAnnouncement.objects.get(pk=job_announcement_id)
            job_announcement.job_title = data['job_title']
            job_announcement.job_description = data['job_description']
            job_announcement.branch = branch
            job_announcement.jobNature = jobNature
            job_announcement.main_skill = data['job_title']  # Set main skill as job title
            job_announcement.soft_skill = data.get('preferredToKnow')
            job_announcement.preferredToKnow = data.get('preferredToKnow')
            job_announcement.gender = data['gender']
            job_announcement.educationLevel = data['educationLevel']
            job_announcement.salary = float(data['salary'])
            job_announcement.type_of_employment = data['type_of_employment']
            job_announcement.experience = int(data['experience'])
            job_announcement.isAvailable = bool(data.get('isAvailable', True))
            job_announcement.save()

            return JsonResponse({'message': 'Job announcement updated successfully'}, status=200)
        else:
            job_announcement = JobAnnouncement.objects.create(
                job_title=data['job_title'],
                job_description=data['job_description'],
                branch=branch,
                jobNature=jobNature,
                main_skill=data['job_title'],  # Set main skill as job title
                soft_skill=data.get('preferredToKnow'),
                preferredToKnow=data.get('preferredToKnow'),
                gender=data['gender'],
                educationLevel=data['educationLevel'],
                salary=float(data['salary']),
                type_of_employment=data['type_of_employment'],
                experience=int(data['experience']),
                isAvailable=bool(data.get('isAvailable', True))
            )
            return JsonResponse({'message': 'Job announcement created successfully'}, status=201)
    except Branch.DoesNotExist:
        return JsonResponse({'error': 'Branch not found.'}, status=404)
    except JobNature.DoesNotExist:
        return JsonResponse({'error': 'Job nature not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def get_all_job_announcements(request):
    logger.debug("Starting to fetch all job announcements.")
    try:
        job_announcements = JobAnnouncement.objects.select_related('branch', 'branch__company').filter(isAvailable=True)
        results = []
        for job in job_announcements:
            logger.debug(f"Processing job announcement: {job.jobAnnouncement_id}")
            result = {
                'jobAnnouncement_id': job.jobAnnouncement_id,
                'job_title': job.job_title,
                'job_description': job.job_description,
                'branch_name': job.branch.name,
                'branch_city': job.branch.city,
                'company_name': job.branch.company.company_name,
                'isAvailable': job.isAvailable,
                'createdAt': job.createdAt.strftime('%Y-%m-%d'),
                'preferredToKnow':job.preferredToKnow,
                'experience': job.experience,
                'educationLevel': job.educationLevel,
                'salary': job.salary,
                'type_of_employment': job.type_of_employment,
                'gender': job.gender,
            }
            results.append(result)
            logger.debug(f"Added job announcement to results: {job.jobAnnouncement_id}")
        
        logger.debug("Successfully fetched and processed all job announcements.")
        return JsonResponse({'results': results}, safe=False)
    except Exception as e:
        logger.error(f"Error fetching job announcements: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
    
@require_GET
def get_job_announcement_info(request, job_id):
    try:
        job_announcement = JobAnnouncement.objects.select_related('branch', 'branch__company', 'jobNature').get(pk=job_id)
        job_info = {
            'jobAnnouncement_id': job_announcement.jobAnnouncement_id,
            'job_title': job_announcement.job_title,
            'preferredToKnow': job_announcement.preferredToKnow,
            'job_description': job_announcement.job_description,
            'branch_name': job_announcement.branch.name,
            'branch_city': job_announcement.branch.city,
            'company_name': job_announcement.branch.company.company_name,
            'jobNature': job_announcement.jobNature.name,
            'image_path': job_announcement.branch.image,
            'gender': job_announcement.gender,
            'educationLevel': job_announcement.educationLevel,
            'salary': job_announcement.salary,
            'type_of_employment': job_announcement.type_of_employment,
            'experience': job_announcement.experience,
        }
        return JsonResponse(job_info)
    except JobAnnouncement.DoesNotExist:
        return JsonResponse({'error': 'Job announcement not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@require_POST
def apply_for_job(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        job_announcement_id = data.get('job_announcement_id')

        if not user_id or not job_announcement_id:
            return JsonResponse({'error': 'User ID and Job Announcement ID are required.'}, status=400)

        user = User.objects.get(pk=user_id)
        job_announcement = JobAnnouncement.objects.get(pk=job_announcement_id)

        # Check if the user has already applied for this job
        if AppliedJob.objects.filter(user=user, jobAnnouncement=job_announcement).exists():
            return JsonResponse({'error': 'User has already applied for this job.'}, status=400)

        # Create the applied job record
        applied_job = AppliedJob.objects.create(
            user=user,
            jobAnnouncement=job_announcement,
            status='Waiting'
        )

        return JsonResponse({'message': 'Job application submitted successfully'}, status=201)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
    except JobAnnouncement.DoesNotExist:
        return JsonResponse({'error': 'Job announcement not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_applied_job(request, user_id, appliedJob_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        applied_job = get_object_or_404(AppliedJob, pk=appliedJob_id, user=user)

        # Deleting the specified applied job
        applied_job.delete()

        return JsonResponse({'message': 'Applied job successfully deleted.'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
    except AppliedJob.DoesNotExist:
        return JsonResponse({'error': 'Applied job not found or does not belong to the specified user.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_GET
def get_applied_jobs_for_announcement(request, job_announcement_id):
    try:
        job_announcement = JobAnnouncement.objects.get(pk=job_announcement_id)

        # Get all applied jobs for the specific job announcement
        applied_jobs = AppliedJob.objects.filter(jobAnnouncement=job_announcement)

        applied_jobs_data = []
        for applied_job in applied_jobs:
            applied_jobs_data.append({
                'appliedJob_id': applied_job.appliedJob_id,
                'jobAnnouncement_id': applied_job.jobAnnouncement.jobAnnouncement_id,
                'job_title': applied_job.jobAnnouncement.job_title,
                'preferredToKnow':applied_job.jobAnnouncement.preferredToKnow,
                'job_description': applied_job.jobAnnouncement.job_description,
                'branch_name': applied_job.jobAnnouncement.branch.name,
                'branch_city': applied_job.jobAnnouncement.branch.city,
                'company_name': applied_job.jobAnnouncement.branch.company.company_name,
                'jobNature': applied_job.jobAnnouncement.jobNature.name,
                'isAvailable': applied_job.jobAnnouncement.isAvailable,
                'createdAt': applied_job.jobAnnouncement.createdAt,
                'gender': applied_job.jobAnnouncement.gender,
                'educationLevel': applied_job.jobAnnouncement.educationLevel,
                'salary': applied_job.jobAnnouncement.salary,
                'type_of_employment': applied_job.jobAnnouncement.type_of_employment,
                'experience': applied_job.jobAnnouncement.experience,
                'user_id': applied_job.user.user_id,
                'user_first_name': applied_job.user.firstName,
                'user_last_name': applied_job.user.lastName,
                'status': applied_job.status,
                'current_date': applied_job.current_date,
            })

        return JsonResponse({'applied_jobs': applied_jobs_data}, status=200)
    except JobAnnouncement.DoesNotExist:
        return JsonResponse({'error': 'Job announcement not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_GET
def get_applied_jobs_for_user(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        # Sort the applied jobs by 'current_date' in descending order
        applied_jobs = AppliedJob.objects.filter(user=user, jobAnnouncement__isAvailable=True).order_by('-current_date')

        applied_jobs_data = []
        for applied_job in applied_jobs:
            branch_name = applied_job.jobAnnouncement.branch.name
            message = get_custom_message(applied_job.status, user.firstName, branch_name)
            applied_jobs_data.append({
                'appliedJob_id': applied_job.appliedJob_id,
                'jobAnnouncement_id': applied_job.jobAnnouncement.jobAnnouncement_id,
                'job_title': applied_job.jobAnnouncement.job_title,
                'branch_name': branch_name,
                'status_name': get_status_name(applied_job.status),
                'message': message,
                'current_date': applied_job.current_date.strftime('%d-%m-%Y'),
            })
        response_data ={
            'length': len(applied_jobs_data),
            'users': applied_jobs_data
        }
        return JsonResponse({'result': response_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@csrf_exempt
@require_POST
def update_or_create_applied_job_status(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        job_announcement_id = data.get('job_announcement_id')
        new_status = data.get('status')

        if not user_id or not job_announcement_id or not new_status:
            return JsonResponse({'error': 'User ID, Job Announcement ID, and status are required.'}, status=400)

        user = get_object_or_404(User, pk=user_id)
        job_announcement = get_object_or_404(JobAnnouncement, pk=job_announcement_id)

        if new_status not in ['Waiting', 'Accepted', 'Rejected', 'To be Interviewed']:
            return JsonResponse({'error': 'Invalid status provided.'}, status=400)

        applied_job, created = AppliedJob.objects.get_or_create(
            user=user,
            jobAnnouncement=job_announcement,
            defaults={'status': 'Waiting'}
        )

        applied_job.status = new_status
        applied_job.save()

        if new_status == 'Accepted':
            message = (
                f"Dear {user.firstName},\n\n"
                "Congratulations on being accepted for the position of "
                f"{job_announcement.job_title} at {job_announcement.branch.name}. We are excited to welcome you to our team.\n\n"
                "Please await further instructions regarding the next steps in the onboarding process.\n\n"
                "Best regards,\n"
                f"{job_announcement.branch.name} Team"
            )

        elif new_status == 'Rejected':
            message = (
                f"Dear {user.firstName},\n\n"
                "Thank you for your interest in the position of {job_announcement.job_title} at {job_announcement.branch.name}. "
                "After careful consideration, we regret to inform you that we have decided not to proceed with your application.\n\n"
                "We appreciate your effort and encourage you to apply for future opportunities that match your skills and experience.\n\n"
                "Best wishes,\n"
                f"{job_announcement.branch.name} Team"
            )

        elif new_status == 'To be Interviewed':
            interview_details = data.get('date'), data.get('time'), data.get('place')
            if not all(interview_details):
                return JsonResponse({'error': 'Complete date, time, and place information is required for scheduling an interview.'}, status=400)

            interview_date = datetime.strptime(data['date'], '%d-%m-%Y').date()
            interview_time = datetime.strptime(data['time'], '%H:%M').time()

            Interview.objects.update_or_create(
                user=user,
                job_announcement=job_announcement,
                defaults={
                    'date': interview_date,
                    'time': interview_time,
                    'place': data['place'],
                    'message': f"Interview scheduled on {interview_date.strftime('%d-%m-%Y')} at {interview_time.strftime('%H:%M')} in {data['place']}."
                }
            )

            message = (
                f"Dear {user.firstName},\n\n"
                "We are pleased to invite you to an interview for the position of "
                f"{job_announcement.job_title} at {job_announcement.branch.name}. Your interview is scheduled on "
                f"{interview_date.strftime('%d-%m-%Y')} at {interview_time.strftime('%H:%M')} in {data['place']}.\n\n"
                "Please confirm your availability for the scheduled time.\n\n"
                "Best regards,\n"
                f"{job_announcement.branch.name} Team"
            )

        else:
            message = f"Your application status for {job_announcement.job_title} at {job_announcement.branch.name} has been updated to {new_status}."

        return JsonResponse({'message': message}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
    except JobAnnouncement.DoesNotExist:
        return JsonResponse({'error': 'Job announcement not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@require_GET
def get_latest_notification(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        # Retrieve the latest interview for the user based on date and time
        interview = Interview.objects.filter(user=user).order_by('-date', '-time').first()

        if not interview:
            return JsonResponse({'message': 'No notifications available.'}, status=200)

        return JsonResponse({'notification': interview.message}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt  
@require_POST
def toggle_is_available(request, job_announcement_id):
    try:
        job_announcement = JobAnnouncement.objects.get(pk=job_announcement_id)
        job_announcement.isAvailable = not job_announcement.isAvailable
        job_announcement.save()
        return JsonResponse({'message': 'Job availability status toggled successfully.'})
    except JobAnnouncement.DoesNotExist:
        return JsonResponse({'error': 'Job announcement not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_GET
def get_all_job_natures(request):
    try:
        job_natures = JobNature.objects.all()
        job_natures_data = [{'jobNature_id': job_nature.jobNature_id, 'name': job_nature.name} for job_nature in job_natures]
        return JsonResponse({'job_natures': job_natures_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
@require_POST
def add_job_nature(request):
    try:
        data = json.loads(request.body)
        job_nature_name = data.get('name')

        if not job_nature_name:
            return JsonResponse({'error': 'Job nature name is required.'}, status=400)

        # Check if the job nature already exists
        if JobNature.objects.filter(name=job_nature_name).exists():
            return JsonResponse({'error': 'Job nature already exists.'}, status=400)

        # Create the job nature record
        job_nature = JobNature.objects.create(name=job_nature_name)

        return JsonResponse({'message': 'Job nature created successfully', 'id': job_nature. jobNature_id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_GET
def list_users_with_matching_job_nature(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    job_announcements = JobAnnouncement.objects.filter(branch=branch)
    skills = Skill.objects.filter(user=user)
    best_skill = max(skills, key=lambda skill: skill.experience, default=None)
    best_skill_name = best_skill.skill if best_skill else None
    
    # Extract job natures from the branch's job opportunities
    job_natures = set(job_announcement.jobNature.jobNature_id for job_announcement in job_announcements)
    
    matching_users = []

    users = User.objects.all()
    for user in users:
        user_job_natures = set(skill.jobNature.jobNature_id for skill in user.skill_set.all())
        if job_natures.intersection(user_job_natures):
            matching_users.append(user)

    # Serialize user data
    user_data = [
        {
            'user_id': user.user_id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'image': user.photo,
            'city': user.city,
            'address':user.address,
            'best_skill': best_skill_name,
            'gender': user.gender
        }
        for user in matching_users
    ]

    response_data = {
        'length': len(user_data),
        'users': user_data
    }

    return JsonResponse(response_data)

@csrf_exempt
@require_POST
def job_filtered(request):
    try:
        data = json.loads(request.body)
        city = data.get('city')
        branch_name = data.get('branch_name')
        sort_order = data.get('sort_order')
        search_term = data.get('search_term')

        # Start with all job announcements
        job_announcements = JobAnnouncement.objects.all()

        # Filter by city if provided
        if city:
            job_announcements = job_announcements.filter(branch__city=city)

        # Filter by branch name if provided
        if branch_name:
            branches = Branch.objects.filter(name__icontains=branch_name)
            job_announcements = job_announcements.filter(branch__in=branches)

        # Filter by job title if provided
        if search_term:
            job_announcements = job_announcements.filter(job_title__icontains=search_term)

        # Multi-criteria sorting: first by salary if provided, then always by date
        if sort_order == 'high':
            job_announcements = job_announcements.order_by('-salary', '-createdAt')
        elif sort_order == 'low':
            job_announcements = job_announcements.order_by('salary', '-createdAt')
        else:
            # Default sort by newest first if no salary sort is specified
            job_announcements = job_announcements.order_by('-createdAt')

        job_data = [
            {
                'jobAnnouncement_id': job.jobAnnouncement_id,
                'job_title': job.job_title,
                'branch': job.branch.name,
                'experience': job.experience,
                'city': job.branch.city,
                'job_nature':job.jobNature.name,
                'branch': job.branch.name,
                'branch_image': job.branch.image,
                'experience': job.experience,
                'type':job.type_of_employment,
                'createdAt': job.createdAt.strftime('%d-%m-%Y')  # Format date as Day-Month-Year
            }
            for job in job_announcements
        ]

        response_data = {
            'length': len(job_data),
            'jobs': job_data
        }

        return JsonResponse(response_data, safe=False)  # Use safe=False if you are returning a list
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_GET
def get_branch_job_announcements(request, branch_id):
    try:
        # Get the branch object or return a 404 if not found
        branch = get_object_or_404(Branch, pk=branch_id)

        # Retrieve job announcements for the branch and sort them by creation date (newest first)
        job_announcements = JobAnnouncement.objects.filter(branch=branch).order_by('-createdAt')

        # Prepare the data for the response
        job_data = [
            {
                'jobAnnouncement_id': job.jobAnnouncement_id,
                'job_title': job.job_title,
                'branch': job.branch.name,
                'experience': job.experience,
                'city': job.branch.city,
                'job_nature': job.jobNature.name,
                'branch_image': job.branch.image,
                'type': job.type_of_employment,
            }
            for job in job_announcements
        ]

        # Return the response
        return JsonResponse({'jobs': job_data, 'count': len(job_data)}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)