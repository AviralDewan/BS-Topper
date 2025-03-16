from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from student_auth.models import StudentUser
from .serializers import StudentUserSerializer

@api_view(['POST'])
def register_student(request):
    if request.method == 'POST':
        try:
            if 'username' not in request.data or 'password' not in request.data or 'first_name' not in request.data or 'last_name' not in request.data:
                return Response({"message": "Missing field(s)"}, status=status.HTTP_400_BAD_REQUEST)

            if StudentUser.objects.filter(username=request.data.get('username')).exists():
                return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = StudentUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)
            
            return Response({"error": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({"error": "An error occured, user could not be registered"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
