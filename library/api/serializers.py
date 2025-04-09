from rest_framework import serializers
from library.models import Resource, ResourceSection, Row
from student_auth.models import StudentUser
from student_auth.api.serializers import StudentUserSerializer

class RowSerializer(serializers.ModelSerializer):
    created_by = StudentUserSerializer()

    class Meta:
        model = Row
        fields = "__all__"

class ResourceSectionSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True)
    created_by = StudentUserSerializer()

    class Meta:
        model = ResourceSection
        fields = ["name", "desc", "created_by", "created_on", "rows"]

class ResourceSerializer(serializers.ModelSerializer):
    sections = ResourceSectionSerializer(many=True)
    created_by = StudentUserSerializer()

    class Meta:
        model = Resource
        fields = ["name", "desc", "tag", "created_by", "created_on", "sections"]
