import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from student_auth.models import StudentUser
from .models import Course, Lecture, TimeStamp

def get_current_program_level_details(request):
    data = {
        'programs': [program for program in StudentUser.LEVEL_CHOICES],
        'levels': [level for level in StudentUser.PROGRAM_CHOICES]
    }

    return JsonResponse(data)

def get_course_list(request):
    data = {
        'courses': [{'name': course.name, 'level': course.level, 'program': course.program} for course in Course.objects.all()]
    }

    return JsonResponse(data)

def get_weeks_and_lectures(request, course_id):
    
    course = Course.objects.get(id=course_id)
    week_list = set(lecture.week_name for lecture in Lecture.objects.filter(course=course))

    weekwise_data = {
        week_name: [{
            'lecture_name': lecture.name,
            'lecture_number': lecture.lecture_number,
            'video_link': lecture.video_link,
            'duration': lecture.duration
        } for lecture in Lecture.objects.filter(week_name=week_name)] for week_name in week_list
    }

    return JsonResponse(weekwise_data)

def get_timestamps(request, lecture_id):

    if request.user.is_authenticated:

        lecture = Lecture.objects.get(id=lecture_id)
        student = StudentUser.objects.get(id=request.user.id)
        data = {
            timestamp.id: [timestamp.start_timestamp, timestamp.end_timestamp] for timestamp in TimeStamp.objects.filter(lecture=lecture, student=student)
        }

        return JsonResponse(data)
    
    return HttpResponse('You must be logged in to perform this action')

def save_timestamps(request):
    if request.method == 'POST':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')

        start_timestamp = request.POST.get('start_timestamp')
        end_timestamp = request.POST.get('end_timestamp')
        lecture_id = request.POST.get('lecture_id')
        student_id = request.user.id

        if not start_timestamp:
            return HttpResponse('Provide timestamp')
        
        if not lecture_id:
            return HttpResponse('Provide lecture id')

        lecture = Lecture.objects.get(id=lecture_id)
        student = StudentUser.objects.get(id=student_id)
        timestamp = TimeStamp.objects.create(lecture=lecture, student=student, start_timestamp=start_timestamp, end_timestamp=end_timestamp)

        return HttpResponse('Timestamp created')
    
    return HttpResponse('Incorrect REST method')

def ai_help(request):
    # if start/end timestamps not provided then take whole lecture as scope
    return HttpResponse('AI help')
