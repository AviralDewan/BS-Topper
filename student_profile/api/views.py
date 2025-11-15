from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from student_auth.models import StudentUser
from student_profile.models import NewsLetter, Todo
from student_auth.api.serializers import StudentUserSerializer
from django.utils import timezone

@api_view(['GET'])
def get_profile_details(request, pk):
    
    if request.method == 'GET':
        try:

            if not StudentUser.objects.filter(id=pk).exists():
                return Response({"message": "Student with provided ID doesn't exist"}, status=status.HTTP_200_OK)

            student = StudentUser.objects.get(id=pk)
            
            serializer = StudentUserSerializer(student)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "An error occured, couldn't load student profile"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_profile_details(request):

    try:
        
        serializer = StudentUserSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  
            # return Response(serializer.data)
            return Response({"message": "Profile details updated"}, status=status.HTTP_200_OK)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as error:
        return Response({"error": "An error occured, couldn't save changes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
@api_view(["PUT"])
def add_to_newsletter(request):
    try:
        email = request.data.get("email")

        if not email:
            return Response({"error": "Please enter your email"}, status=status.HTTP_404_BAD_REQUEST)

        if not NewsLetter.objects.filter(email=email).exists():
            NewsLetter.objects.create(email=email)
        
        return Response({"success": "Successfully added to newsletter"}, status=status.HTTP_200_OK)
    except:
        return Response({"error": "An error occured, couldn't add email to newsletter"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_todo(request):
    try:
        
        todo = request.data.get("todo")
        if not todo:
            return Response({"warning": "Enter todo name"}, status=status.HTTP_400_BAD_REQUEST)
        elif todo:
            todo = Todo.objects.create(todo=todo, student=request.user)
            todo.save()
            return Response({"message": "Todo created"}, status=status.HTTP_201_CREATED)
        
        return Response({"warning": "Enter todo name"}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as error:
        return Response({"error": "An error occured, couldn't create todo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_todo(request):
    try:
        
        todoList = Todo.objects.filter(student=request.user).order_by('-addedOn')

        todos = [{"todo": todoItem.todo, "checked": todoItem.checked, "addedOn": todoItem.addedOn, "completedOn": todoItem.completedOn, "id": todoItem.id} for todoItem in todoList]

        return Response({"todos": todos}, status=status.HTTP_201_CREATED)
        
    except Exception as error:
        return Response({"error": "An error occured, couldn't get todos"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_todo(request):
    try:
        
        info = request.data.get("info")
        id = request.data.get("id")
        
        if not id:
            return Response({"error": "Please share id"}, status=status.HTTP_400_BAD_REQUEST)

        todo = Todo.objects.get(id=id)

        if request.user != todo.student:
            return Response({"error": "Please enter the information to be updated"}, status=status.HTTP_400_BAD_REQUEST)

        if info:
            mode = info.get("mode")
            if mode == "todo":
                if len(info.get("todo").strip()) > 0:
                    todo.todo = info.get("todo")
                    todo.save()
                    return Response({"message": "Todo updated"}, status=status.HTTP_200_OK)
            elif mode == "checked":
                if todo.checked:
                    todo.checked = False
                    todo.completedOn = None
                else:
                    todo.checked = True
                    todo.completedOn = timezone.now()
                todo.save()
                return Response({"message": "Todo updated"}, status=status.HTTP_200_OK)
        
        return Response({"error": "Please enter the information to be updated"}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as error:
        print(error)
        return Response({"error": "An error occured, couldn't update todo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_todo(request):
    try:
        
        id = request.data.get("id")

        todo = Todo.objects.get(id=id)

        if request.user == todo.student:
            todo.delete()
        
        return Response({"message": "Todo deleted"}, status=status.HTTP_200_OK)
        
    except Exception as error:
        return Response({"error": "An error occured, couldn't delete todo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)