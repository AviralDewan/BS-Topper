from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
import logging
from student_auth.models import StudentUser
from groups.models import Group, GroupMembership, Post, PinnedPost, Comment, PostVotes
from .serializers import GroupSerializer, GroupMembershipSerializer, PostSerializer, CommentSerializer
from .permissions import IsAdminOrNoGroup, IsAdmin, IsPoster, isCommenter
from rest_framework.throttling import UserRateThrottle
from .pagination import Paginator

logging.basicConfig(level=logging.ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrNoGroup])
def create_group(request):
    print(request.data)
    if request.method == "POST":

        try:

            serializer = GroupSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save(admin=request.user)
                group = Group.objects.get(name=request.data["name"])
                membership = GroupMembership.objects.create(group=group, student=request.user)
                return Response({"message": "Group created", "data": serializer.data, "id": group.id}, status=status.HTTP_200_OK)
            
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": "An error occured, couldn't create group."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_group(request):
    if request.method == "PUT":
        try:
            group_id = request.data.get("group_id")

            group = Group.objects.get(id=group_id)

            permission = IsAdmin()
            if not permission.has_object_permission(request, None, group):
                return Response({"message": permission.message}, status=status.HTTP_403_FORBIDDEN)

            serializer = GroupSerializer(group, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Group info updated"}, status=status.HTTP_200_OK)
            
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Group.DoesNotExist:
            return Response({"message": "Group doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": "An error occured, couldn't save changes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def is_group_member(group, new_admin):
    return GroupMembership.objects.filter(group=group, student=new_admin).exists()

def is_not_admin(new_admin):
    return Group.objects.filter(admin=new_admin).count() == 0

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_admin(request):
    if request.method == "PUT":
        try:
            if "new_admin_id" not in request.data:
                return Response({"message":"Please select the new admin"}, status=status.HTTP_400_BAD_REQUEST)

            new_admin_id = request.data.get("new_admin_id")
            new_admin = StudentUser.objects.get(id=new_admin_id)

            group = Group.objects.filter(admin=request.user)[0]

            permission = IsAdmin()
            if not permission.has_object_permission(request, None, group):
                return Response({"message": permission.message}, status=status.HTTP_403_FORBIDDEN)
            
            if not is_group_member(group, new_admin):
                return Response({"message": "Only group members can be promoted to admin"}, status=status.HTTP_400_BAD_REQUEST)
            if not new_admin.is_staff and not is_not_admin(new_admin):
                return Response({"message": "Student should not be the admin of another group"}, status=status.HTTP_400_BAD_REQUEST)

            group.admin = new_admin
            group.save()

            return Response({"message": "Group admin updated"}, status=status.HTTP_200_OK)
        
        except Group.DoesNotExist:
            return Response({"message": "You don't have the permission to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
        except StudentUser.DoesNotExist:
            return Response({"error": "Selected student doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": "An error occured, couldn't change admin"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_group_member(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        is_member = GroupMembership.objects.filter(group=group, student=request.user).exists()
        return Response({"is_member": is_member}, status=status.HTTP_200_OK)
    except Group.DoesNotExist:
        return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_group(request):
    if request.method == "POST":
        
        group_id = request.data.get("group_id")

        if not group_id:
            return Response({"message": "Please provide group ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = request.user

            if not Group.objects.filter(id=group_id).exists():
                return Response({"message": "Group doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

            group = Group.objects.get(id=group_id)

            if GroupMembership.objects.filter(group=group, student=student).exists():
                return Response({"message": "You are already a member"}, status=status.HTTP_200_OK)
            
            serializer = GroupMembershipSerializer(data={"group": group.id, "student": request.user.id})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Group joined"}, status=status.HTTP_200_OK)

            return Response({"message": "Couldn't join group"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logging.exception("Group joining error")
            return Response({"error": "An error occured, couldn't join group"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def leave_group(request):
    if request.method == "DELETE":
        
        group_id = request.data.get("group_id")

        if not group_id:
            return Response({"message": "Please provide group ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = request.user

            if student.username == "admin":
                return Response({"message": "You cannot perform this action"}, status=status.HTTP_400_BAD_REQUEST)

            if not Group.objects.filter(id=group_id).exists():
                return Response({"message": "Group doesn't exist"},status=status.HTTP_400_BAD_REQUEST)

            group = Group.objects.get(id=group_id)

            if not GroupMembership.objects.filter(group=group, student=student).exists():
                return Response({"message": "You must be a group member to perform this action"},status=status.HTTP_400_BAD_REQUEST)
            
            group_membership = GroupMembership.objects.get(group=group, student=student)

            if request.user == group.admin:
                group.admin = StudentUser.objects.get(username="admin")
                group.save()
            
            group_membership.delete()

            return Response({"message": "Group left"},status=status.HTTP_200_OK)

        except Exception:
            logging.exception("Leaving group")
            return Response({"error": "An error occured, couldn't leave group"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_my_groups(request):
    if request.method == "GET":
        
        try:
            if request.GET.get("id"):
                pkey = request.GET.get("id")
                student = StudentUser.objects.get(pk=pkey)
            else:
                return Response({"error": "An error occured, couldn't get groups"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # student = request.user

            membership = GroupMembership.objects.filter(student=student)
            if not membership.exists():
                return Response({"message": "No groups joined"}, status=status.HTTP_200_OK)

            groups = [membership.group for membership in membership]

            paginator = Paginator()
            paginated_groups = paginator.paginate_queryset(groups, request)
            serializer = GroupSerializer(paginated_groups, many=True, context={"request": request})
            
            return paginator.get_paginated_response(serializer.data)
        except Exception:
            logging.exception("Get my Groups")
            return Response({"message": "An error occured, couldn't get groups"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def get_groups_list(request):
    try:
        
        group_list = [(group.id, group.name) for group in Group.objects.all()]

        return Response({"data": group_list}, status=status.HTTP_200_OK)

    except Exception:
        return Response({"error": "An error occured, couldn't get group names"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def make_post(request):
    
    if request.method == 'POST':
        
        try:
            student = request.user

            required_fields = ["title", "content", "group"]

            if [field for field in required_fields if field not in request.data]:
                return Response({"message": "Please provide the required information"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not Group.objects.filter(id=request.data.get("group")).exists():
                return Response({"message": "Group doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            
            group = Group.objects.get(id=request.data.get("group"))

            if not GroupMembership.objects.filter(group=group, student=student).exists():
                return Response({"message": "You must be a member of the group to post"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = PostSerializer(data=request.data)

            if serializer.is_valid():
                post = serializer.save(poster=student)
                return Response({"message": "Post created", "id": post.id}, status=status.HTTP_201_CREATED)
            
            return Response({"message": "Post not created"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        except Exception:
            logging.exception("Making Post")
            return Response({"error": "An error occured, post couldn't be created"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_my_posts(request):

    if request.method == "GET":
        
        try:
            if request.GET.get("id"):
                pkey = request.GET.get("id")
                student = StudentUser.objects.get(pk=pkey)
            else:
                return Response({"error": "An error occured, couldn't get posts"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # student = request.user
            if "group_id" in request.GET:
                if not Group.objects.filter(id=request.GET["group_id"]).exists():
                    return Response({"message":"Group doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
                group = Group.objects.get(id=request.GET["group_id"])
                posts = Post.objects.filter(group=group, poster=student).order_by('-posted_on')
            else:
                posts = Post.objects.filter(poster=student).order_by('-posted_on')
            
            paginator = Paginator()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(paginated_posts, many=True, context={"request": request})
                
            return paginator.get_paginated_response(serializer.data)
        except Exception:
            logging.exception("Get my posts")
            return Response({"error": "An error occured, couldn't get posts"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def view_posts(request, group_id):
    
    if request.method == "GET":

        try:

            if not Group.objects.filter(id=group_id).exists():
                return Response({"message": "Group doesn\'t exist"}, status=status.HTTP_400_BAD_REQUEST)
            
            group = Group.objects.get(id=group_id)

            posts = Post.objects.filter(group=group).order_by('-posted_on')

            paginator = Paginator()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(paginated_posts, many=True)
            
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            logging.exception("View Posts")
            return Response({"error": "An error occured, coudldn't get posts."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def view_post(request, post_id):

    if request.method == "GET":

        try:
            if not Post.objects.filter(id=post_id).exists():
                return Response({"message": "Post doesn\'t exist"}, status=status.HTTP_400_BAD_REQUEST)

            post = Post.objects.get(id=post_id)
            comments = Comment.objects.filter(post=post)

            serializer = PostSerializer(post, context={"request": request})
            serializerComments = CommentSerializer(comments, context={"request": request}, many=True)

            return Response({"post": serializer.data, "comments": serializerComments.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"error": "An error occured, couldn't get post"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):

    if request.method == "DELETE":
        try:
            if not "group_id" in request.data:
                return Response({"message": "Please share Group ID"}, status=status.HTTP_400_BAD_REQUEST)
            
            group_id = request.data["group_id"]
            
            group = Group.objects.get(id=group_id)
            student = request.user
            admin = group.admin
            
            post = Post.objects.get(id=post_id)

            is_poster = IsPoster()
            if not is_poster.has_object_permission(request, None, post):
                return Response({"message": is_poster.message}, status=status.HTTP_403_FORBIDDEN)
            
            pinned = getattr(post, 'pinned_post', None)
            if pinned:
                pinned.delete()
            post.delete()

            return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            return Response({"message": "Group doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"message": "Post doesn\'t exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logging.exception("Post Deletion")
            return Response({"error": "An error occured, Post couldn't be deleted"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def get_pinned_post(request, group_id):

    if request.method == "GET":
        
        try:
            group = Group.objects.get(id=group_id)

            if not PinnedPost.objects.filter(group=group).exists():
                return Response({"message": "No pinned post for this Group"}, status=status.HTTP_200_OK)
            
            pinned_post = PinnedPost.objects.get(group=group)

            if not pinned_post.post:
                return Response({"message": "No pinned post for this Group"}, status=status.HTTP_200_OK)
            
            serializer = PostSerializer(pinned_post.post, context={"request": request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Group.DoesNotExist:
            return Response({"message": "Group doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "An error occured, couldn't get pinned post"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_pinned_post(request, group_id):

    if request.method == "POST":
        
        try:
            
            if "post_id" not in request.data:
                return Response({"message": "Please share post to be pinned"}, status=status.HTTP_400_BAD_REQUEST)

            post_id = request.data["post_id"]
            group = Group.objects.get(id=group_id)
            post = Post.objects.get(id=post_id)

            permission = IsAdmin()
            if not permission.has_object_permission(request, None, group):
                return Response({"message": permission.message}, status=status.HTTP_403_FORBIDDEN)

            if post.group != group:
                return Response({"message": "Only posts in current group can be pinned"}, status=status.HTTP_400_BAD_REQUEST)

            if PinnedPost.objects.filter(group=group).exists():
                pinned_post = PinnedPost.objects.get(group=group)
                pinned_post.objects.delete()
            
            pinned_post = PinnedPost.objects.create(group=group, post=post)
            
            serializer = PostSerializer(pinned_post.post, context={"request": request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Group.DoesNotExist:
            return Response({"error": "Group doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "Post doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logging.exception("Set pinned post")
            return Response({"error": "An error occured, couldn't set pinned post"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_comment(request, post_id):

    if request.method == "POST":

        try:
        
            if "comment" not in request.data:
                return Response({"message": "Please share the comment"}, status=status.HTTP_400_BAD_REQUEST)
            
            post = Post.objects.get(id=post_id)
            poster = request.user

            serializer = CommentSerializer(data=request.data, context={"request": request, "post": post})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Comment added"}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            return Response({"message": "Post doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logging.exception("Post Comment")
            return Response({"error": "An error occured, comment couldn't be posted"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, post_id):

    if request.method == "DELETE":
        try:
        
            student = request.user

            if not "comment_id" in request.data:
                return Response({"message": "Please share comment ID"}, status=status.HTTP_400_BAD_REQUEST)
            
            comment_id = request.data["comment_id"]
            
            comment = Comment.objects.get(id=comment_id)

            permission = isCommenter()
            if not permission.has_object_permission(request, None, comment):
                return Response({"message": permission.message}, status=status.HTTP_403_FORBIDDEN)

            comment.delete()

            return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"message": "Comment doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logging.exception("Comment Deletion")
            return Response({"error": "An error occured, comment couldn't be deleted"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def toggle_vote(request, post_id):

    if request.method == "PUT":
        
        try:
            student = request.user
            
            post = Post.objects.get(id=post_id)

            if PostVotes.objects.filter(post=post, student=student).exists():
                postvote = PostVotes.objects.get(post=post, student=student)
                postvote.delete()
            else:
                postvote = PostVotes.objects.create(post=post, student=student)
            
            return Response({"message": PostVotes.objects.filter(post=post).count()}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"message": "Post doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logging.exception("Toggle Vote")
            return Response({"error": "An error occured, couldn't toggle vote"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
