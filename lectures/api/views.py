from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from collections import defaultdict
from student_auth.models import StudentUser
from .DSscores import foundation
from .DSscores import diploma
from .DSscores import degree
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
        print(e)
        return Response({"error": "An error occured, couldn't get course list"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
def get_test_fields(request):
    try:
        program = request.query_params.get("program")
        level = request.query_params.get("level")
        course_id = request.query_params.get("course")

        if not program or not level or not course_id:
            return Response({"message": "Please enter the required information"}, status=status.HTTP_400_BAD_REQUEST)

        program, level = program.strip().upper(), level.strip().upper()

        print(program, level, course_id)

        if program not in [program[0].upper() for program in StudentUser.PROGRAM_CHOICES] or level not in [level[0].upper() for level in StudentUser.LEVEL_CHOICES]:
            return Response({"message": "Invalid program or level"}, status=status.HTTP_400_BAD_REQUEST)

        if level in ["DP", "DG"] or program in ["ES"]:
            return Response({"coming_soon": "This feature will be coming soon"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Course.objects.filter(id=course_id, program=program, level=level).exists():
            return Response({"message": "Course doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.get(program=program, level=level, id=course_id)

        if level == "FL":
            fields = foundation.test_fields(course.code)
        if level == "DP":
            fields = diploma.test_fields(course.code)
        elif level == "DG":
            fields = degree.test_fields(course.code)
        
        return Response({"course_name": course.name, "data": fields}, status=status.HTTP_200_OK)

    except Exception as e:
        print(str(e))
        return Response({"error": "An error occured, couldn't get test fields"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["POST"])
def calc_score(request):
    try:
        program = request.data.get("program")
        level = request.data.get("level")
        course_id = request.data.get("course_id")
        marks_list = request.data.get("marks_list")

        if not program or not level or not course_id or not marks_list:
            return Response({"message": "Please enter the required information"}, status=status.HTTP_400_BAD_REQUEST)

        program, level = program.strip().upper(), level.strip().upper()

        if program not in [program[0].upper() for program in StudentUser.PROGRAM_CHOICES] or level not in [level[0].upper() for level in StudentUser.LEVEL_CHOICES]:
            return Response({"message": "Invalid program or level"}, status=status.HTTP_400_BAD_REQUEST)

        if level in ["DP", "DG"] or program in ["ES"]:
            return Response({"coming_soon": "This feature will be coming soon"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Course.objects.filter(id=course_id, program=program, level=level).exists():
            return Response({"message": "Course doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        course = Course.objects.get(program=program, level=level, id=course_id)

        if level == "FL":
            current_status, marks_coordinates, resources = foundation.calc_score(course.code, marks_list)
        
        return Response({"current_status": current_status, "marks_coordinates": marks_coordinates, "resources": resources}, status=status.HTTP_200_OK)

    except Exception as e:
        print(str(e))
        return Response({"error": "An error occured, couldn't predict grade"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

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
        return Response({"error": "An error occured, couldn't save time stamp"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
def ai_help(request):
    # if start/end timestamps not provided then take whole lecture as scope
    return HttpResponse('AI help')
