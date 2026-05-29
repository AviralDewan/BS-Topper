from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from student_auth.models import Student
from .serializers import StudentSerializer

class SignupView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


