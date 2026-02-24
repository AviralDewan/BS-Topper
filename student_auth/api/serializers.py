from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from student_auth.models import StudentUser, EventRegistration, EventSubmission

class StudentUserSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentUser model.
    """
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = StudentUser
        fields = [
            "id",
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
        
        if StudentUser.objects.all().filter(username=value.strip()).exists():
            raise serializers.ValidationError("Username is already taken. Choose another.")
        
        return value.strip()

    def validate_first_name(self, value):
        """
        Ensures first name is not empty.
        """
        if len(value.strip()) == 0:
            return value
        # if not value.strip():
        #     raise serializers.ValidationError("First name cannot be empty.")
        return value

    def validate_last_name(self, value):
        """
        Ensures last name is not empty.
        """
        if len(value.strip()) == 0:
            return value
        # if not value.strip():
        #     raise serializers.ValidationError("Last name cannot be empty.")
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
    
    def validate_roll_number(self, value):

        if len(value.strip()) == 0:
            return value

        if " " in value or "f" not in value or len(value.strip()) > 10:
            raise serializers.ValidationError("Invalid roll number")
        
        return value
    
    def validate_bio(self, value):

        if len(value.strip()) == 0:
            return value

        if len(value.strip()) > 150:
            raise serializers.ValidationError("Bio length must be less than 150 characters")
        
        return value

    def to_representation(self, instance):
        """
        Removes null or empty fields from the response.
        """
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value not in [None, "", []]}


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = "__all__"

    def validate_email(self, value):
        if "iitm.ac.in" not in value.split("@")[-1]:
            raise serializers.ValidationError("Only IITM email allowed")
        return value.lower()

    def validate(self, data):
        event_type = data.get("event_type")

        if not data.get("accepted_rules"):
            raise serializers.ValidationError("Rules must be accepted")

        return data


class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventSubmission
        fields = "__all__"
        # extra_kwargs = {
        #     field: {"required": True, "allow_null": False, "allow_blank": False}
        #     for field in [
        #         "name",
        #         "event_id",
        #         "event_type",
        #         "email",
        #         "level",
        #         "house",
        #         "awarness",
        #         "phone",
        #         "permission_for_social",
        #         "agree_to_rules",
        #         "submission_link",
        #     ]
        # }

    def validate_email(self, value):
        value = value.lower()

        if not value.endswith("@iitm.ac.in"):
            raise serializers.ValidationError("Only IITM email allowed.")

        return value

    def validate_submission_link(self, value):
        if not value.startswith("https://drive.google.com/"):
            raise serializers.ValidationError("Submission must be a Google Drive link.")

        return value

    def validate_agree_to_rules(self, value):
        if value != "Yes":
            raise serializers.ValidationError("You must agree to the rules to submit.")

        return value

    # def validate(self, attrs):
    #     # Extra safety: ensure absolutely nothing is missing
    #     for field in self.Meta.extra_kwargs.keys():
    #         if not attrs.get(field):
    #             raise serializers.ValidationError({field: "This field is required."})

    #     return attrs