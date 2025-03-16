from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import StudentUser

def signup_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        if not username or not password or not first_name or not last_name:
            return HttpResponse('Missing field(s)')
        
        username = username.strip()
        password = password.strip()
        first_name = first_name.strip()
        last_name = last_name.strip()
        
        if len(password) < 8 or ' ' in password:
            return HttpResponse('Password length should be more than 8, password should not contain spaces')

        if ' ' in first_name or ' ' in last_name:
            return HttpResponse('Name can\'t have spaces')

        if StudentUser.objects.filter(username=username).exists():
            return HttpResponse('User already exists')

        user = StudentUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()

        return HttpResponse('User created')
    
    return HttpResponse('Incorrect REST method')

def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return HttpResponse('Missing username or password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse('Logged in')
        
        return HttpResponse('Invalid username or password')
    
    return HttpResponse('Incorrect REST method')

def logout_student(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse('User logged out')
    return HttpResponse('You must be logged in to perform this action')
