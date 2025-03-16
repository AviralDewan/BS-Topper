from rest_framework import serializers
from student_auth.models import StudentUser

class StudentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentUser
        fields = "__all__"

    def validate_username(self, value):
        if ' ' in value:
            raise serializers.ValidationError("Username can't have spaces")
        return value
    
    def validate_first_name(self, value):
        if ' ' in value:
            raise serializers.ValidationError("Name can't have spaces")
        return value

    def validate_last_name(self, value):
        if ' ' in value:
            raise serializers.ValidationError("Name can't have spaces")
        return value
    
    def validate_password(self, value):
        if len(value) < 8 or ' ' in value:
            raise serializers.ValidationError('Password length should be more than 8, password should not contain spaces')
        return value
