from rest_framework import serializers
from resources.models import Resource
from student_auth.models import Student

class ResourceSerializer(serializers.ModelSerializer):
    creator_profile_url = serializers.HyperlinkedRelatedField(source="creator", view_name="student_view", read_only=True)
    creator_username = serializers.CharField(source="creator.username", read_only=True, allow_null=True)
    class Meta:
        model = Resource
        fields = "__all__"
    
    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.extend(["creator_profile_url", "creator_username"])
        return fields

