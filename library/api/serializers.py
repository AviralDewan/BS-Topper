from rest_framework import serializers
from library.models import Resource, ResourceSection, Row
from student_auth.models import StudentUser
from student_auth.api.serializers import StudentUserSerializer

class RowSerializer(serializers.ModelSerializer):
    created_by = StudentUserSerializer(read_only=True)
    resource_section = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Row
        fields = "__all__"
    
    def create(self, validated_data):
        context = self.context
        validated_data["resource_section"] = context["resource_section"]
        validated_data["created_by"] = context["student"]
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        context = self.context
        name = validated_data.get("name")
        link = validated_data.get("link")
        if name and Row.objects.filter(resource_section=context["resource_section"], name=name.strip()).exists():
            raise serializers.ValidationError("Row with same name exists in the Resource Section")
        if link and Row.objects.filter(resource_section=context["resource_section"], link=link.strip()).exists():
            raise serializers.ValidationError("Row with same link exists in the Resource Section")
        return super().update(instance, validated_data)

class ResourceSectionSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True, read_only=True)
    created_by = StudentUserSerializer(read_only=True)

    class Meta:
        model = ResourceSection
        fields = ["name", "desc", "created_by", "created_on", "rows"]
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.save()
        super().update(instance, validated_data)
        return instance

class ResourceSerializer(serializers.ModelSerializer):
    sections = ResourceSectionSerializer(many=True, read_only=True)
    created_by = StudentUserSerializer(read_only=True)

    class Meta:
        model = Resource
        fields = ["name", "desc", "tag", "created_by", "created_on", "sections"]
    
    def update(self, instance, validated_data):
        name = validated_data.get("name")
        tag = validated_data.get("tag")
        tag_choices = [tag[0] for tag in Resource.TAG_CHOICES]

        same_name_resource = Resource.objects.filter(name=name)
        if name and same_name_resource.exists() and same_name_resource == instance:
            raise serializers.ValidationError("A resource with the same name exists")
        if tag and tag not in tag_choices:
            raise serializers.ValidationError(f"Tag must be one of {tag_choices}")

        return super().update(instance, validated_data)
