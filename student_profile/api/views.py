from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from student_auth.models import StudentUser
from student_auth.api.serializers import StudentUserSerializer

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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_profile_details(request):
    try:
        
        serializer = StudentUserSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
            return Response({"message": "Profile details updated"}, status=status.HTTP_200_OK)
        
        return Response({"error": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as error:
        return Response({"error": "An error occured, couldn't save changes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            