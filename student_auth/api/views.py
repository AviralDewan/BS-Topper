from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from student_auth.models import StudentUser, BootcampRegister
from .serializers import StudentUserSerializer

@api_view(['POST'])
def register_student(request):
    # print(request.data)
    if request.method == 'POST':
        try:

            serializer = StudentUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)
            
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(error)
            return Response({"error": "An error occured, user could not be registered"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def signup(request):
    if 'name' not in request.data or 'roll' not in request.data or 'phone' not in request.data:
        return Response('Please fill all fields')
    
    name, roll, phone = request.data["name"], request.data["roll"], request.data["phone"]

    try:
        student = BootcampRegister.objects.get_or_create(name=name, roll=roll, phone=phone)

        return Response('Registered successfully!')
    except Exception as e:
        return Response('An error occured, couldn\'t register')
