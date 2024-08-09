from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST , require_GET
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from .models import Company, Branch
from job.models import JobAnnouncement , JobNature
from users.models import User
from skills.models import Skill
import json
from hireme.skills import skills

@csrf_exempt
@require_POST
def create_branch(request):
    try:
        data = json.loads(request.body)
        print(f"Creating branch with data: {data}")
        company_data = data.get('company')
        if not company_data or 'company_name' not in company_data:
            return JsonResponse({'error': 'Company data with company_name is required.'}, status=400)

        company_name = company_data['company_name']
        company, created = Company.objects.get_or_create(company_name=company_name)
        print(f"Company {'created' if created else 'found'}: {company.company_name}")

        branch = Branch.objects.create(
            name=data['name'],
            company=company,
            phone_number = data['phone_number'],
            city=data['city'],
            emails=data['emails'],  
            user_name=data['user_name'],
            password=data['password'],
            user_type= 2 
        )
        print(f"Branch created: {branch.name}, ID: {branch.id}")
        return JsonResponse({'message': 'Branch created successfully', 'branch_id': branch.id}, status=201)
    except Exception as e:
        print(f"Error creating branch: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)



@require_GET
def get_branch_info(request, branch_id):
    try:
        branch = get_object_or_404(Branch, pk=branch_id)
        branch_info = {
            'branch_id': branch.branch_id,
            'username': branch.user_name,
            'password': branch.password,
            'email':branch.emails,
            'phone_number': branch.phone_number,
            'branch_name': branch.name,
            'branch_city': branch.city,
            'company_name': branch.company.company_name,
            'image': branch.image
        }
        print(f"Retrieved info for branch ID {branch_id}")
        return JsonResponse(branch_info, safe=False)
    except Branch.DoesNotExist:
        print(f"Branch not found: {branch_id}")
        return JsonResponse({'error': 'Branch not found'}, status=404)
    except Exception as e:
        print(f"Error retrieving branch info: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

    
@require_GET
def get_all_companies(request):
    try:
        companies = Company.objects.all()
        companies_list = [{
            'company_id': company.company_id,
            'company_name': company.company_name
        } for company in companies]
        return JsonResponse({'results': companies_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@require_GET
def get_all_branches(request):
    try:
        print("Fetching all branches...")
        branches = Branch.objects.select_related('company').all()
        branches_data = []
        for branch in branches:
            branches_data.append({
                'branch_id': branch.branch_id,
                'name': branch.name,
                'company_name': branch.company.company_name,
                'address': branch.address,
                'city': branch.city,
                'user_name': branch.user_name,
                'image': branch.image
            })
        print(f"Total branches retrieved: {len(branches_data)}")
        return JsonResponse({'branches': branches_data}, status=200)
    except Exception as e:
        print(f"Error retrieving branches: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

    
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_branch_image(request, branch_id):
    try:
        print(f"Attempting to upload image for branch ID: {branch_id}")
        branch = Branch.objects.get(branch_id=branch_id)
        file = request.FILES.get('image')
        if not file:
            print("No file uploaded")
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_path = os.path.join(settings.MEDIA_ROOT, 'branch_images', file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        branch.image = os.path.join('media', 'branch_images', file.name)
        branch.save()
        print(f"Image successfully uploaded and saved at: {branch.image}")
        return Response({'message': 'Image uploaded successfully', 'image_path': branch.image}, status=status.HTTP_200_OK)
    except Branch.DoesNotExist:
        print("Branch not found")
        return Response({'error': 'Branch not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error during image upload: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@require_GET
def get_announcements_by_branch(request, branch_id):
    try:
        print(f"Fetching job announcements for branch ID: {branch_id}")
        branch = get_object_or_404(Branch, pk=branch_id)
        job_announcements = JobAnnouncement.objects.filter(branch=branch).order_by('-createdAt')
        announcements_data = [
            {
                'jobAnnouncement_id': job.jobAnnouncement_id,
                'branch_name': job.branch.name,
                'branch_image': job.branch.image,
                'branch_city': job.branch.city,
                'jobNature': job.jobNature.name,
                'job_title': job.job_title,
                'experience': job.experience,
                'type_of_employment': job.type_of_employment,
                'createdAt': job.createdAt.strftime('%Y-%m-%d')  # Adjusted date format to Y-m-d
            }
            for job in job_announcements
        ]
        print(f"Total announcements fetched: {len(announcements_data)}")
        return JsonResponse({'length': len(announcements_data), 'announcements': announcements_data}, status=200)
    except Exception as e:
        print(f"Error fetching announcements: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

    
@csrf_exempt
@require_POST
def filter_users(request, branch_id):
    try:
        print(f"Filtering users for branch ID: {branch_id}")
        data = json.loads(request.body)
        city = data.get('city')
        gender = data.get('gender')
        skill_name = data.get('skill')
        branch = get_object_or_404(Branch, pk=branch_id)
        job_natures = JobNature.objects.filter(jobannouncement__branch=branch).distinct()
        users = User.objects.all()
        
        if city:
            users = users.filter(city__iexact=city)
        if gender and gender.lower() != "any":
            users = users.filter(gender__iexact=gender)
        if skill_name:
            users = users.filter(skill__skill_name__icontains=skill_name, skill__jobNature__in=job_natures).distinct()
        
        user_data = [{
            'user_id': user.user_id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'image': user.photo,
            'city': user.city,
            'address': user.address,
            'best_skill': best_skill.skill if (best_skill := max(Skill.objects.filter(user=user), key=lambda skill: skill.experience, default=None)) else None,
            'gender': user.gender
        } for user in users]
        print(f"Total users matching criteria: {len(user_data)}")
        return JsonResponse({'length': len(user_data), 'users': user_data})
    except Exception as e:
        print(f"Error filtering users: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def get_skills_by_branch_job_nature(request, branch_id):
    try:
        # Get the branch and related job announcements
        branch = get_object_or_404(Branch, pk=branch_id)
        job_announcements = JobAnnouncement.objects.filter(branch=branch)

        # Extract job natures from the branch's job opportunities
        job_natures = set(job_announcement.jobNature.name for job_announcement in job_announcements)

        # Filter skills based on job natures present in the branch's job announcements
        matching_skills = []
        for nature in job_natures:
            if nature in skills:
                matching_skills.extend(skills[nature])

        response_data = {
            'job_natures': list(job_natures),
            'skills': matching_skills
        }

        return JsonResponse(response_data, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)