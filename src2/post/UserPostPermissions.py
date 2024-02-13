from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from post.models import PostPermission


class PostDeletePermission(permissions.BasePermission):
    "Permission Denied"
    def has_permission(self, request, view) -> bool:
        print(request.method)
        if request.method == 'DELETE':
            return PostPermission.objects.filter(user=request.user, can_delete_post=True).exists()
        return True