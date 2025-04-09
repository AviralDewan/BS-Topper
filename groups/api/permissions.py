from rest_framework import permissions
from groups.models import Group

class IsAdminOrNoGroup(permissions.BasePermission):
    message = "You can be the admin of only 1 group at a time"

    def has_permission(self, request, view):
        if request.method in ["POST", "PUT", "DELETE"]:
            return request.user.is_staff or Group.objects.filter(admin=request.user).count() == 0
        return True

class IsAdmin(permissions.BasePermission):
    message = "Only admin can perform this action"

    def has_object_permission(self, request, view, obj):
        if request.method in ["POST",  "PUT", "DELETE"]:
            return request.user.is_staff or obj.admin == request.user
        return True

class IsPoster(permissions.BasePermission):
    message = "You don't have the permission to perform this action"

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.is_staff or obj.poster == request.user
        return False

class isCommenter(permissions.BasePermission):
    message = "You don't have the permission to perform this action"

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.is_staff or obj.poster == request.user or obj.post.group.admin == request.user
        return False
