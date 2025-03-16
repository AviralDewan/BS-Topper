import json
import re
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from student_auth.models import StudentUser

def get_profile_details(request, student_id):
    
    if request.method == 'GET':
        student = StudentUser.objects.get(id=student_id)

        if student is None:
            return HttpResponse('Student not found')

        student_data = {
            'username': student.username,
            'first name': student.first_name,
            'last name': student.last_name,
            'program': student.program,
            'level': student.level,
            'date joined': student.date_joined, 
            'mobile number': student.mobile_number, 
            'bio': student.bio,
            'profile picture': student.profile_pic, 
            'roll number': student.roll_number, 
            'email': student.email
        }

        return JsonResponse(student_data)
    
    return HttpResponse('Incorrect REST method')

def check_valid_mobile(mobile_number):
    return re.search(r'[abcdefghijklmnopqrstuvwxyz!@#$%^&*()_-]',mobile_number.lower()) or mobile_number.count('+') > 1 or mobile_number[0] != '+'

def edit_profile_details(request):

    if request.method == 'PUT':
        if not request.user.is_authenticated:
            return redirect('login')
        
        data = json.loads(request.body)
        student = StudentUser.objects.get(id=request.user.id)

        if 'username' in data:
            if StudentUser.objects.filter(username=data['username']).exists():
                return HttpResponse('Username taken, select another username')
            student.username=data['username']
        if 'password' in data:
            student.set_password(data['password'])
        if 'first_name' in data:
            student.first_name = data['first_name']
        if 'last_name' in data:
            student.last_name = data['last_name']
        if 'program' in data:
            if data['program'] not in [program[0] for program in student.PROGRAM_CHOICES]:
                return HttpResponse('Please select correct program')
            student.program = data['program']
        if 'level' in data:
            if data['level'] not in [level[0] for level in student.LEVEL_CHOICES]:
                return HttpResponse('Please select correct level')
            student.level = data['level']
        if 'date_joined' in data:
            student.date_joined = data['date_joined']
        if 'mobile_number' in data:
            if check_valid_mobile(data['mobile_number']):
                return HttpResponse('Invalid mobile number')
            student.mobile_number = data['mobile_number']
        if 'bio' in data:
            student.bio = data['bio']
        if 'profile_picture' in data:
            student.profile_pic = data['profile_picture']
        if 'roll_no' in data:
            student.roll_no = data['roll_no']
        if 'email' in data:
            student.email = data['email']
        
        student.save()
        return HttpResponse('Data updated')
    
    return HttpResponse('Incorrect REST method')
        