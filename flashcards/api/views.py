from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from student_auth.models import StudentUser
from lectures.models import Lecture
from flashcards.models import Flashcard

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_or_create_flashcard(request, lecture_id):
    
    try:
        lec = Lecture.objects.get(id=lecture_id)
        
        question, answer = request.data.get("question"), request.data.get("answer")
        
        fc = Flashcard.objects.filter(lecture=lec, student=request.user)
        if fc.exists():
            return Response({"id": fc[0].id, "question": fc[0].question, "answer": fc[0].answer}, status=status.HTTP_200_OK)

        if question is None or answer is None:
            return Response({"error": "Please enter all details"}, status=status.HTTP_400_BAD_REQUEST)

        fc = Flashcard.objects.create(student=request.user, lecture=lec, question=question, answer=answer)

        return Response({"id": fc.id, "question": fc.question, "answer": fc.answer}, status=status.HTTP_201_CREATED)
    except Lecture.DoesNotExist:
        return Response({"message": "Lecture not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_flashcard(request, fc_id):
    try:
        
        fc = Flashcard.objects.get(id=fc_id)

        return Response({"flashcard": {"question": fc.question, "answer": fc.answer, "lec_id": fc.lecture.id}}, status=status.HTTP_200_OK)

    except Flashcard.DoesNotExist:
        return Response({"message": "Flashcard not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_flashcard(request, fc_id):
    try:
        
        fc = Flashcard.objects.get(id=fc_id)
        
        question, answer = request.data.get("question"), request.data.get("answer")

        if question is None and answer is None:
            return Response({"message": "Please share details to update"}, status=status.HTTP_400_BAD_REQUEST)
        
        if question:
            fc.question = question
        if answer:
            fc.answer = answer
        
        fc.save()

        return Response({"flashcard": {"question": fc.question, "answer": fc.answer}}, status=status.HTTP_200_OK)
    except Flashcard.DoesNotExist:
        return Response({"message": "Flashcard not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_flashcard(request, fc_id):
    try:
        
        fc = Flashcard.objects.get(id=fc_id)
        fc.question = ""
        fc.answer = ""
        fc.save()

        return Response({"message": "Flashcard deleted"}, status=status.HTTP_200_OK)

    except Flashcard.DoesNotExist:
        return Response({"message": "Flashcard not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def get_all(request):
    try:
        
        flevel, fcourse = request.query_params.get("level"), request.query_params.get("course")

        fcList = Flashcard.objects.all()

        fcData = []

        for fc in fcList:
            if fc.question == "" or fc.answer == "":
                continue
            if flevel is not None and flevel != fc.lecture.course.level:
                continue
            if fcourse is not None and int(fcourse) != fc.lecture.course.id:
                continue
            
            level = "Degree"
            if fc.lecture.course.level == "FL":
                level = "Foundation"
            elif fc.lecture.course.level == "DP":
                level = "Diploma"
            fcDict = {
                "id": fc.id,
                "poster": {
                    "name": fc.student.username,
                    "profile_pic": fc.student.profile_pic,
                    "id": fc.student.id
                },
                "course": fc.lecture.course.name,
                "level": level,
                "name": fc.lecture.name,
                "question": fc.question,
                "answer": fc.answer,
                "lec_id": fc.lecture.id,
                "lec": f"{fc.lecture.week_number}.{fc.lecture.lecture_number}"
            }
            fcData.append(fcDict)

        return Response({"flashcards": fcData}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_flashcards(request):
    try:
        
        flevel, fcourse = request.query_params.get("level"), request.query_params.get("course")

        fcList = Flashcard.objects.filter(student=request.user)

        fcData = []

        for fc in fcList:
            if fc.question == "" or fc.answer == "":
                continue
            if flevel is not None and flevel != fc.lecture.course.level:
                continue
            if fcourse is not None and int(fcourse) != fc.lecture.course.id:
                continue
            
            level = "Degree"
            if fc.lecture.course.level == "FL":
                level = "Foundation"
            elif fc.lecture.course.level == "DP":
                level = "Diploma"
            fcDict = {
                "poster": {
                    "name": fc.student.username,
                    "profile_pic": fc.student.profile_pic
                },
                "id": fc.id,
                "course": fc.lecture.course.name,
                "level": level,
                "name": fc.lecture.name,
                "question": fc.question,
                "answer": fc.answer
            }
            fcData.append(fcDict)

        return Response({"flashcards": fcData}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

