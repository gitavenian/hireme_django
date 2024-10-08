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
from job.models import JobAnnouncement
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
        print("Attempting to retrieve user...")
        user = get_object_or_404(User, pk=user_id)
        print(f"User retrieved: {user.username}")

        file = request.FILES.get('photo')
        if not file:
            print("No file uploaded")
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"File received: {file.name}")
        
        # Construct file path within media directory
        file_path = os.path.join(settings.MEDIA_ROOT, 'user_photos', file.name)
        print(f"Saving file to: {file_path}")

        # Save file to the specified path
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        print("File saved successfully")

        # Update user photo path
        user.photo = os.path.join('media', 'user_photos', file.name)
        user.save()
        print(f"Updated user photo path: {user.photo}")

        return Response({'message': 'Photo uploaded successfully', 'image_path': user.photo}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        print("User not found")
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
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
            print("Received request body:", request.body)  # Print raw request body
            data = json.loads(request.body)
            print("Parsed JSON data:", data)  # Print parsed data

            required_fields = ['firstName', 'lastName', 'username', 'password', 'email', 'birthDate', 'address', 'city', 'educationLevel', 'gender', 'phone_number']
            
            # Check if all required fields are present in the request data
            if not all(field in data for field in required_fields):
                missing_fields = [field for field in required_fields if field not in data]
                print("Missing fields:", missing_fields)  # Print which fields are missing
                return JsonResponse({'error': 'Missing required fields', 'missing_fields': missing_fields}, status=400)

            # Format the birthDate to ISO 8601 format
            try:
                birth_date = datetime.fromisoformat(data['birthDate'].split('T')[0])  # Splits the datetime string at 'T' and takes only the date part
            except ValueError as e:
                print("Birthdate format error:", e)  # Print error if the date format is incorrect
                return JsonResponse({'error': 'Birthdate format is incorrect. Please use YYYY-MM-DD format.'}, status=400)

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
            print("User created successfully:", user.username)  # Confirm user creation
            return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201)
        except Exception as e:
            print("Exception occurred:", str(e))  # Print any other exception error
            return JsonResponse({'error': str(e)}, status=400)
    else:
        print("Invalid request method:", request.method)  # Notify about invalid method
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
        user = get_object_or_404(User, pk=user_id)
        age = calculate_age(user.birthDate)

        skills = Skill.objects.filter(user=user)
        best_skill = max(skills, key=lambda skill: skill.experience, default=None)
        best_skill_name = best_skill.skill_name
        best_skill_data = {
            'skill_id': best_skill.skill_id,
            'jobNature_id': best_skill.jobNature.jobNature_id,
            'jobNature_name': best_skill.jobNature.name,
            'skill_name': best_skill.skill_name,
            'description': best_skill.description,
            'experience': best_skill.experience,
            'started_at': best_skill.started_at,
        } if best_skill else None

        previous_jobs = PreviousJob.objects.filter(user=user)
        best_job = max(previous_jobs, key=lambda job: job.experience, default=None)
        best_job_data = {
            'previousJob_id': best_job.previousJob_id,
            'jobNature_id': best_job.jobNature.jobNature_id,
            'jobNature_name': best_job.jobNature.name,
            'job_name': best_job.job_name,
            'start_date': best_job.start_date,
            'end_date': best_job.end_date,
            'experience': best_job.experience,
            'portfolio': best_job.portfolio,
            'description': best_job.description,
            'recommendation': best_job.recommendation,
        } if best_job else None

        user_info = {
            'user_id': user.user_id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'best_skill': best_skill_name,
            'email': user.email,
            'age': age,
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
            'experience': best_job_data,
            'skill': best_skill_data
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
    
@csrf_exempt
@require_POST
def update_social_media_links(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        data = json.loads(request.body)
        
        user.facebook_link = data.get('facebook_link', user.facebook_link)
        user.behance_link = data.get('behance_link', user.behance_link)
        user.instagram_link = data.get('instagram_link', user.instagram_link)
        user.github_link = data.get('github_link', user.github_link)
        
        user.save()
        
        return JsonResponse({'message': 'Social media links updated successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
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

@require_GET
def get_branches_by_user_skill_natures(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    # Get the unique set of job natures linked to the user's skills
    user_job_natures = {skill.jobNature for skill in Skill.objects.filter(user=user)}
    
    # Fetch all job announcements that have a job nature matching the user's skill natures
    matching_job_announcements = JobAnnouncement.objects.filter(jobNature__in=user_job_natures).distinct()
    
    # Extract unique branches from these job announcements
    branches = {announcement.branch.name for announcement in matching_job_announcements}
    
    # Prepare the list of branch names
    branch_names = list(branches)
    
    # Return the list of branch names as JSON
    return JsonResponse({'branches': branch_names, 'count': len(branch_names)})