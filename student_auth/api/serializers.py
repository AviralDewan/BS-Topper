from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from student_auth.models import StudentUser

class StudentUserSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentUser model.
    """
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = StudentUser
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "program",
            "level",
            "date_joined",
            "bio",
            "profile_pic",
            "roll_number",
            "email",
            "mobile_number",
            "profile_url"
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def get_profile_url(self, obj):
        return f"https://bs-topper/get-profile-details/{obj.username}/"

    def create(self, validated_data):
        """
        Hashes the password before saving a new user.
        """
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Hashes password on update if provided.
        """
        if "password" in validated_data:
            instance.password = make_password(validated_data.pop("password"))
        return super().update(instance, validated_data)

    def validate_username(self, value):
        """
        Ensures username has no spaces and is unique.
        """
        if " " in value:
            raise serializers.ValidationError("Username cannot contain spaces.")
        
        if StudentUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken. Choose another.")
        
        return value

    def validate_first_name(self, value):
        """
        Ensures first name is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        return value

    def validate_last_name(self, value):
        """
        Ensures last name is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Last name cannot be empty.")
        return value

    def validate_password(self, value):
        """
        Ensures password is at least 8 characters long and has no spaces.
        """
        if len(value) < 8 or " " in value:
            raise serializers.ValidationError("Password must be at least 8 characters long and cannot contain spaces.")
        return value

    def validate_program(self, value):
        """
        Ensures program selection is valid.
        """
        valid_choices = dict(StudentUser.PROGRAM_CHOICES).keys()
        if value not in valid_choices:
            raise serializers.ValidationError("Invalid program choice.")
        return value

    def validate_level(self, value):
        """
        Ensures level selection is valid.
        """
        valid_choices = dict(StudentUser.LEVEL_CHOICES).keys()
        if value not in valid_choices:
            raise serializers.ValidationError("Invalid level choice.")
        return value

    def to_representation(self, instance):
        """
        Removes null or empty fields from the response.
        """
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value not in [None, "", []]}
