from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET , require_POST
from company.models import Branch
from .models import User
from django.utils.dateparse import parse_date
import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from skills.models import PreviousJob, Skill
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime , date
import json
def calculate_age(birthdate):
    today = date.today()
    if birthdate is None:
        return None
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_photo(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        
        file = request.FILES.get('photo')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save file to media directory
        file_path = os.path.join(settings.MEDIA_ROOT, 'user_photos', file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Update user photo path
        user.photo = os.path.join('media', 'user_photos', file.name)
        user.save()
        
        return Response({'message': 'Photo uploaded successfully', 'image_path': user.photo}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@require_GET
def get_user_credentials(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return JsonResponse({
        'username': user.username,
        'password': user.password 
    }, safe=True)


def update_user_credentials(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        data = json.loads(request.body)
        username = data.get('username')
        new_password = data.get('password')

        if username:
            user.username = username

        if new_password:
            user.password = new_password 

        user.save()
        return JsonResponse({'message': 'Credentials updated successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_GET
def get_user_image(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        image_url = user.photo if user.photo else None
        message = 'User has no image' if not image_url else 'Image URL retrieved successfully'
        return JsonResponse({'user_id': user.user_id, 'image_url': image_url, 'message': message}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def get_user_languages(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        languages = user.language.split(',') if user.language else []
        return JsonResponse({'languages': languages}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_GET
def get_user_education_level(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        education_level = user.educationLevel

        return JsonResponse({'user_id': user.user_id, 'educationLevel': education_level}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_POST
def delete_language(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        languages_to_delete = data.get('languages')
        
        if not user_id or not languages_to_delete:
            return JsonResponse({'error': 'User ID and languages are required.'}, status=400)
        
        user = User.objects.get(pk=user_id)
        
        current_languages = user.language.split(',') if user.language else []
        updated_languages = [language for language in current_languages if language not in languages_to_delete]
        
        user.language = ','.join(updated_languages)
        user.save()
        
        return JsonResponse({'message': 'Languages deleted successfully.'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
@require_POST
def manage_language(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        languages = data.get('languages')

        if not user_id or languages is None:
            return JsonResponse({'error': 'User ID and languages are required.'}, status=400)
        
        user = User.objects.get(pk=user_id)
        
        if user.language:
            # Add new languages to the current set
            current_languages = user.language.split(',') if user.language else []
            for language in languages:
                if language not in current_languages:
                    current_languages.append(language)
            user.language = ','.join(current_languages)
        else:
            # Replace current languages with the new set
            user.language = ','.join(languages)
        
        user.save()
        
        return JsonResponse({'message': 'Languages updated successfully.'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['firstName', 'lastName', 'username', 'password', 'email', 'birthDate', 'address', 'city', 'educationLevel', 'gender', 'phone_number']
            
            # Check if all required fields are present in the request data
            if not all(field in data for field in required_fields):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Format the birthDate to dd-mm-yyyy
            birth_date = datetime.strptime(data['birthDate'], '%d/%m/%Y').date()

            user = User.objects.create(
                firstName=data['firstName'],
                lastName=data['lastName'],
                username=data['username'],
                password=data['password'],
                email=data['email'],
                birthDate=birth_date,
                address=data['address'],
                city=data['city'],
                educationLevel=data['educationLevel'],
                gender=data['gender'],
                phone_number=data['phone_number'],
                user_type=User.NORMAL
            )
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@require_POST
def update_user_personal_info(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        data = json.loads(request.body)

        # Extract fields from JSON body
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        home_address = data.get('home_address')
        email = data.get('email')
        city = data.get('city')
        birth_date = data.get('birth_date')
        gender = data.get('gender')

        # Update fields if provided
        if first_name is not None:
            user.firstName = first_name
        if last_name is not None:
            user.lastName = last_name
        if home_address is not None:
            user.address = home_address
        if email is not None:
            user.email = email
        if city is not None:
            user.city = city
        if birth_date is not None:
            user.birthDate = parse_date(birth_date)
        if gender is not None:
            user.gender = gender

        user.save()

        return JsonResponse({'message': 'User information updated successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def login_view(request):
    try:
        data = json.loads(request.body)
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        if not username_or_email or not password:
            return JsonResponse({'error': 'Please provide both username/email and password'}, status=400)

        # Check User model
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = None

        if user and user.password == password:
            return JsonResponse({
                'message': 'Login successful',
                'user_id': user.user_id,
                'user_type': user.user_type,
                'firstName': user.firstName,
                'lastName': user.lastName,
            })

        # Check Branch model if not found in User model
        try:
            branch = Branch.objects.get(user_name=username_or_email)
        except Branch.DoesNotExist:
            branch = None

        if branch and branch.password == password:
            return JsonResponse({
                'message': 'Login successful',
                'branch_id': branch.branch_id,
                'user_type': branch.user_type,
                'name': branch.name,
                'company_id': branch.company.company_id,
            })

        return JsonResponse({'error': 'Invalid username/email or password'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        


@require_GET
def get_user_info(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        age = calculate_age(user.birthDate)

        best_skill = max(skills, key=lambda skill: skill.experience, default=None)
        best_skill_name = best_skill.skill if best_skill else None

        # Fetch the user's previous jobs
        previous_jobs = PreviousJob.objects.filter(user=user)
        previous_jobs_data = []
        for job in previous_jobs:
            previous_jobs_data.append({
                'previousJob_id': job.previousJob_id,
                'jobNature_id': job.jobNature.jobNature_id,
                'jobNature_name': job.jobNature.name,
                'job_name': job.job,
                'start_date': job.start_date,
                'end_date': job.end_date,
                'experience': job.experience,
                'portfolio': job.portfolio,
                'description': job.description,
                'recommendation': job.recommendation,
            })

        # Fetch the user's skills
        skills = Skill.objects.filter(user=user)
        skills_data = []
        for skill in skills:
            skills_data.append({
                'skill_id': skill.skill_id,
                'jobNature_id': skill.jobNature.jobNature_id,
                'jobNature_name': skill.jobNature.name,
                'skill_name': skill.skill,
                'description': skill.description,
                'experience': skill.experience,
                'started_at': skill.started_at,
            })

        user_info = {
            'user_id': user.user_id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'best_skill': best_skill_name,
            'email': user.email,
            'age':age,
            'address': user.address,
            'phone_number': user.phone_number,
            'gender': user.gender,
            'photo': user.photo,
            'city': user.city,
            'educationLevel': user.educationLevel,
            'birthDate': user.birthDate,
            'language': user.language,
            'username': user.username,
            'facebook_link': user.facebook_link,
            'behance_link': user.behance_link,
            'github_link': user.github_link,
            'user_type': user.user_type,
            'previous_jobs': previous_jobs_data,
            'skills': skills_data,
        }

        return JsonResponse(user_info)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    


@require_GET
def get_all_users(request):
    try:
        users = User.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                'user_id': user.user_id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'address': user.address,
                'phone_number': user.phone_number,
                'gender': user.gender,
                'photo': user.photo,
                'city': user.city,
                'educationLevel': user.educationLevel,
                'birthDate': user.birthDate,
                'language': user.language,
                'username': user.username,
                'facebook_link': user.facebook_link,
                'behance_link': user.behance_link,
                'github_link': user.github_link,
                'user_type': user.user_type,
            })
        return JsonResponse({'users': user_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def get_all_users(request):
    try:
        users = User.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                'user_id': user.user_id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'address': user.address,
                'phone_number': user.phone_number,
                'gender': user.gender,
                'photo': user.photo,
                'city': user.city,
                'educationLevel': user.educationLevel,
                'birthDate': user.birthDate,
                'language': user.language,
                'username': user.username,
                'facebook_link': user.facebook_link,
                'behance_link': user.behance_link,
                'github_link': user.github_link,
                'user_type': user.user_type,
            })
        return JsonResponse({'users': user_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def get_user_personal_info(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        user_info = {
            'first_name': user.firstName,
            'last_name': user.lastName,
            'address': user.address,
            'email': user.email,
            'city': user.city,
            'birth_date': user.birthDate.strftime('%d-%m-%Y') if user.birthDate else None,
            'gender': user.gender
        }

        return JsonResponse(user_info, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@api_view(['DELETE'])
def delete_photo(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        
        if not user.photo:
            return Response({'error': 'No photo to delete'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the full path of the photo
        photo_path = os.path.join(settings.MEDIA_ROOT, user.photo.replace('media/', ''))
        
        # Delete the photo file if it exists
        if os.path.isfile(photo_path):
            os.remove(photo_path)
        
        # Remove the photo path from the user model
        user.photo = None
        user.save()
        
        return Response({'message': 'Photo deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_social_media_links(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        data = json.loads(request.body)
        
        user.facebook_link = data.get('facebook_link', user.facebook_link)
        user.behance_link = data.get('behance_link', user.behance_link)
        user.instagram_link = data.get('instagram_link', user.instagram_link)
        user.github_link = data.get('github_link', user.github_link)
        
        user.save()
        
        return Response({'message': 'Social media links updated successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@require_GET
def display_user_social_links(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    social_links = {
        'facebook_link': user.facebook_link,
        'behance_link': user.behance_link,
        'instagram_link': user.instagram_link,
        'github_link': user.github_link
    }

    return JsonResponse(social_links)