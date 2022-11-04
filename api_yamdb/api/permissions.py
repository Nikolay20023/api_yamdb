from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class CommentRewiewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif (request.user.is_anonymous and request.method != ['POST',
              'PATCH', 'DELETE']):
            return True
        elif request.user.is_admin:
            return True
        else:
            return False