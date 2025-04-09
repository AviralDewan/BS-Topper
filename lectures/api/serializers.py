from rest_framework import serializers
from student_auth.api.serializers import StudentUserSerializer
from lectures.models import Course, Lecture, TimeStamp

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"

class LectureSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lecture
        fields = "__all__"

class TimeStampSerializer(serializers.ModelSerializer):
    lecture = LectureSerializer(read_only=True)
    lecture_id = serializers.PrimaryKeyRelatedField(queryset=Lecture.objects.all(), write_only=True)
    student = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TimeStamp
        fields = ["id", "name", "start_timestamp", "end_timestamp", "lecture", "lecture_id", "student"]
    
    def create(self, validated_data):
        lecture = validated_data.pop("lecture_id")
        return TimeStamp.objects.create(lecture=lecture, **validated_data)
    
    def validate(self, attrs):
        start = attrs.get("start_timestamp", None)
        end = attrs.get("end_timestamp", None)

        if end and start >= end:
            raise serializers.ValidationError("End time stamp must be after start time stamp")
        
        return attrs

class WeekWiseLectureSerializer(serializers.Serializer):
    week_name = serializers.CharField()
    lectures = LectureSerializer(many=True)
