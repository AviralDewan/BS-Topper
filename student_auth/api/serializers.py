from student_auth.models import Student
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Student
        fields = ["id", "username", "password", "email", "level", "program", "skills"]
    
    def create(self, validated_data):
        skills = validated_data.pop("skills", [])
        student = Student.objects.create_user(
            password=validated_data["password"],
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            level=validated_data.get("level", ""),
            program=validated_data.get("program", "")
        )
        student.skills.set(skills)
        return student
