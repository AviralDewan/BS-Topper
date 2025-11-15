from rest_framework import serializers
from django.urls import reverse
from student_auth.models import StudentUser
from student_auth.api.serializers import StudentUserSerializer
from groups.models import Group, GroupMembership, Post, PinnedPost, Comment, PostVotes

class GroupSerializer(serializers.ModelSerializer):
    admin = StudentUserSerializer(read_only=True)
    admin_profile_link = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    group_link = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"
    
    def get_admin_profile_link(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/student-profile/get-profile-details/{obj.admin.pk}")
        
    def get_group_link(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/groups/get-group-details/{obj.pk}")
        
    def get_posts_count(self, obj):
        return Post.objects.filter(group=obj).count()
    
    def get_member_count(self, obj):
        return len(GroupMembership.objects.filter(group=obj)) or 1

class GroupMembershipSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())  
    student = serializers.PrimaryKeyRelatedField(queryset=StudentUser.objects.all()) 

    class Meta:
        model = GroupMembership
        fields = "__all__"

    def create(self, validated_data):
        return GroupMembership.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.group = validated_data.get('group', instance.group)
        instance.student = validated_data.get('student', instance.student)
        instance.save()
        return instance

class PostSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    post_link = serializers.SerializerMethodField()
    profile_link = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = "__all__"
    
    def get_post_link(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/groups/view-post/{obj.pk}/")
    
    def get_profile_link(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/student-profile/get-profile-details/{obj.poster.id}")
    
    def get_poster(self, obj):
        poster = obj.poster
        return poster.username, poster.profile_pic, poster.id
    
    def get_comment_count(self, obj):
        return Comment.objects.filter(post=obj).count()
    
    def get_votes(self, obj):
        return obj.votes.count()
    
    def get_downvotes(self, obj):
        return obj.downvotes.count()

class PinnedPostSerializer(serializers.ModelSerializer):
    pass

class CommentSerializer(serializers.ModelSerializer):
    poster = StudentUserSerializer(read_only=True)
    profile_link = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "comment", "commented_on", "poster", "profile_link"] 
        extra_kwargs = {"comment": {"required": True}}
    
    def create(self, validated_data):
        request = self.context.get("request")
        post = self.context.get("post")
        if not isinstance(request.user, StudentUser):
            raise serializers.ValidationError({"poster": "Invalid user type"})
        return Comment.objects.create(
            comment = validated_data["comment"],
            poster=request.user,
            post=post
        )
    
    def get_profile_link(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/student-profile/get-profile-details/{obj.poster.pk}")
