from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from student_auth.models import StudentUser
from .serializers import StudentUserSerializer

@api_view(['POST'])
def register_student(request):
    if request.method == 'POST':
        try:

            serializer = StudentUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)
            
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({"error": "An error occured, user could not be registered"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
