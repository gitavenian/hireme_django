from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json
import datetime
import math
from .models import Skill, PreviousJob
from users.models import User
from job.models import JobNature


def calculate_experience(start_date, end_date=None):
    start_year = start_date.year
    end_year = end_date.year if end_date else datetime.datetime.now().year
    years_of_experience = end_year - start_year

    capped_experience = min(years_of_experience, 8)
    if capped_experience <= 1:
        rating = 1
    else:
        rating = 1 + 4 * (math.log(capped_experience) / math.log(8))

    rating = min(rating, 5)
    rating = round(rating, 1)

    return rating

@csrf_exempt
@require_POST
def add_previous_job(request):
    try:
        data = json.loads(request.body)
        required_fields = ['jobNature_id','user_id', 'job_name', 'start_date','company','description']

        print(f"Received data: {data}")

        # Check if all required fields are present in the request data
        if not all(field in data for field in required_fields):
            print("Missing required fields")
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        jobNature = JobNature.objects.get(pk=data['jobNature_id'])
        user = User.objects.get(pk=data['user_id'])
        start_date = datetime.datetime.strptime(data['start_date'], '%d-%m-%Y').date()
        end_date = datetime.datetime.strptime(data['end_date'], '%d-%m-%Y').date() if 'end_date' in data else None

        experience = calculate_experience(start_date, end_date)
        job_name = data['job']

        print(f"Calculated experience: {experience}")

        previous_job = PreviousJob.objects.create(
            jobNature=jobNature,
            user=user,
            job = data['job'],
            job_name=job_name,
            start_date=start_date,
            end_date=end_date,
            company=data['company'],
            experience=experience,
            portfolio=data.get('portfolio'),
            description=data['description'],
            recommendation=data.get('recommendation')
        )

        print(f"Created previous job: {previous_job}")
        skill_name = data['job']
        # Check if the skill already exists
        skill, created = Skill.objects.get_or_create(
            user=user,
            jobNature=jobNature,
            skill = data['job'],
            skill_name=skill_name,
            defaults={'started_at': start_date, 'experience': experience}
        )

        print(f"Skill exists: {not created}, Skill: {skill}")

        # Update the skill's experience and started_at if necessary
        if not created:
            if skill.started_at > start_date:
                skill.started_at = start_date
            skill.experience += experience
            print(f"Updated skill experience: {skill.experience}")
        else:
            skill.experience = experience
            print(f"Created new skill with experience: {skill.experience}")
        skill.save()

        return JsonResponse({'message': 'Previous job added successfully'}, status=201)
    except JobNature.DoesNotExist:
        print("Job nature not found")
        return JsonResponse({'error': 'Job nature not found.'}, status=404)
    except User.DoesNotExist:
        print("User not found")
        return JsonResponse({'error': 'User not found.'}, status=404)
    except Exception as e:
        print(f"Exception occurred: {e}")
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def get_previous_jobs_by_user_id(request, user_id):
    try:
        previous_jobs = PreviousJob.objects.select_related('jobNature').filter(user_id=user_id)
        previous_jobs_data = []
        for previous_job in previous_jobs:
            previous_jobs_data.append({
                'previousJob_id': previous_job.previousJob_id,
                'user_id': previous_job.user.user_id,
                'jobNature_name': previous_job.jobNature.name,
                'job': previous_job.job,
                'company': previous_job.company,
                'start_date': previous_job.start_date,
                'end_date': previous_job.end_date,
                'experience': previous_job.experience,
                'description': previous_job.description,
            })
        return JsonResponse({"previous_job":previous_jobs_data}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_POST
def add_skill(request):
    try:
        data = json.loads(request.body)

        required_fields = ['user_id', 'jobNature_id', 'skill_name', 'started_at']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        user = get_object_or_404(User, pk=data['user_id'])
        job_nature = get_object_or_404(JobNature, pk=data['jobNature_id'])

        started_at = datetime.datetime.strptime(data['started_at'], '%Y-%m-%d').date()
        experience = calculate_experience(started_at)

        # Create and save the skill
        skill, created = Skill.objects.get_or_create(
            user=user,
            jobNature=job_nature,
            skill_name=data['skill_name'],
            skill  = data['skill_name'],
            defaults={'started_at': started_at,'experience': experience, 'description': data.get('description', '')}
        )

        # If the skill already exists, just update the started_at and experience
        if not created:
            if skill.started_at > started_at:
                skill.started_at = started_at
            skill.experience = experience
            skill.save()

        return JsonResponse({'message': 'Skill added successfully', 'skill_id': skill.skill_id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def get_skills_by_user_id(request, user_id):
    try:
        previous_jobs = PreviousJob.objects.filter(user_id=user_id)
    
    # Create a dictionary to count jobs for each skill
        skill_job_counts = {}
        for job in previous_jobs:
            skill_name = job.job_name
            if skill_name in skill_job_counts:
                skill_job_counts[skill_name] += 1
            else:
                skill_job_counts[skill_name] = 1
            skills = Skill.objects.select_related('jobNature').filter(user_id=user_id)
        
        skills_data = []
        for skill in skills:
            skill_name = skill.skill_name
            total_experience = skill.experience
            job_count = skill_job_counts.get(skill_name, 1)
            skill_experience = total_experience / job_count
            skills_data.append({
                'skill_id': skill.skill_id,
                'user_id': skill.user.user_id,
                'jobNature_id': skill.jobNature.jobNature_id,
                'jobNature_name': skill.jobNature.name,
                'skill': skill.skill_name,
                'description': skill.description,
                'experience': skill_experience,
                'started_at': skill.started_at,
            })
        return JsonResponse({'skills': skills_data}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_GET
def get_user_skills(request, user_id):
    try:
        previous_jobs = PreviousJob.objects.filter(user_id=user_id)
    
    # Create a dictionary to count jobs for each skill
        skill_job_counts = {}
        for job in previous_jobs:
            skill_name = job.job_name
            if skill_name in skill_job_counts:
                skill_job_counts[skill_name] += 1
            else:
                skill_job_counts[skill_name] = 1
            skills = Skill.objects.select_related('jobNature').filter(user_id=user_id)
        
        skills_data = []
        for skill in skills:
            skill_name = skill.skill_name
            skills_data.append({
                skill_name
            })
        return JsonResponse({'skills': skills_data}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
