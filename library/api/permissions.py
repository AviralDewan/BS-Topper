from rest_framework.permissions import BasePermission

class IsCreatorOrAdmin(BasePermission):
    message = "You don't have the permission to perform this action"

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "POST", "DELETE"]:
            return request.user.is_staff or obj.created_by == request.user
        return True
