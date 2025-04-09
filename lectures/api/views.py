from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from collections import defaultdict
from student_auth.models import StudentUser
from lectures.models import Course, Lecture, TimeStamp
from .serializers import CourseSerializer, WeekWiseLectureSerializer, TimeStampSerializer
from .pagination import TimeStampPaginator

@api_view(["GET"])
def get_current_program_level_details(request):
    try:

        data = {
            "programs": [program for program in StudentUser.PROGRAM_CHOICES],
            "levels": [level for level in StudentUser.LEVEL_CHOICES]
        }

        return Response({"message": data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "An error occured, couldn't get program details"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
def get_course_list(request):
    try:

        program = request.query_params.get("program", None)
        level = request.query_params.get("level", None)

        if (program and not level) or ((not program and level)):
            return Response({"message": "Please select program and level"}, status=status.HTTP_400_BAD_REQUEST)
        
        if program and level:
            program, level = program.strip().upper(), level.strip().upper()
            program_choices = [program[0] for program in StudentUser.PROGRAM_CHOICES]
            level_choices = [level[0] for level in StudentUser.LEVEL_CHOICES]

            if program not in program_choices or level not in level_choices:
                return Response({"message": "Please select valid program and level"}, status=status.HTTP_400_BAD_REQUEST)

            CourseList = Course.objects.filter(program__iexact=program, level__iexact=level)
        else:
            CourseList = Course.objects.all()

        serializer = CourseSerializer(CourseList, many=True)

        return Response({"message": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "An error occured, couldn't get course list"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
def get_weeks_and_lectures(request, course_id):
    
    try:
        course = Course.objects.get(id=course_id)
        lectures = Lecture.objects.filter(course=course).order_by('week_number')

        week_map = defaultdict(list)
        for lec in lectures:
            week_map[lec.week_name].append(lec)

        data = [
            {
                'week_name': week,
                'lectures': lec_list
            }
            for week, lec_list in week_map.items()
        ]

        serializer = WeekWiseLectureSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({"message": "Course Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error occured, couldn't week and lecture details"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_timestamps(request):

    try:
        
        student = request.user

        if "lecture_id" in request.query_params:
            lecture_id = request.query_params["lecture_id"]
            lecture = Lecture.objects.get(id=lecture_id)
            timestamps = TimeStamp.objects.filter(lecture=lecture, student=request.user)
        else:
            timestamps = TimeStamp.objects.filter(student=request.user)

        paginator = TimeStampPaginator()
        paginated_timestamps = paginator.paginate_queryset(timestamps, request)
        serializer = TimeStampSerializer(paginated_timestamps, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    except Lecture.DoesNotExist:
        return Response({"message": "Lecture Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": "An error occured, couldn't save time stamp"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_timestamps(request, timestamp_id):

    try:

        student = request.user

        timestamp = TimeStamp.objects.get(id=timestamp_id, student=student)

        timestamp.delete()
        
        return Response({"message": "Time stamp deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    except TimeStamp.DoesNotExist:
        return Response({"message": "Time Stamp Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error occured, couldn't save time stamp"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_timestamps(request):

    try:

        lecture_id = request.data.get("lecture_id")
        student = request.user

        lecture = Lecture.objects.get(id=lecture_id)
        
        serializer = TimeStampSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(student=student)
            return Response({"message": "Timestamp created"}, status=status.HTTP_201_CREATED)
        
        return Response({"error": serializer.errors}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    except Lecture.DoesNotExist:
        return Response({"message": "Lecture Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": "An error occured, couldn't save time stamp"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
def ai_help(request):
    # if start/end timestamps not provided then take whole lecture as scope
    return HttpResponse('AI help')
