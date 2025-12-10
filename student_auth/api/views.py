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
    data = request.data

    # 1. Validate required fields
    required_fields = ['name', 'roll', 'phone']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return Response(f"{field.capitalize()} is required", status=400)

    name = data["name"].strip()
    roll = str(data["roll"]).strip()
    phone = str(data["phone"]).strip()

    # 2. Validate phone number
    if not phone.isdigit() or len(phone) < 10:
        return Response("Invalid phone number", status=400)

    # 3. Validate roll number length
    if "@" not in roll or not roll.endswith("iitm.ac.in"):
        return Response("Email must be an IITM email ending with @iitm.ac.in", status=400)


    try:
        # 4. Create or return existing entry
        student, created = BootcampRegister.objects.get_or_create(
            roll=roll,
            defaults={"name": name, "phone": phone}
        )

        if not created:
            return Response("You are already registered!", status=200)

        return Response("Registered successfully!", status=201)

    except Exception as e:
        print("Error:", e)
        return Response("Server error. Could not register.", status=500)
