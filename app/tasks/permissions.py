"""
Custom permissions for Task Manager API
"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a task to view/edit it
    """

    message = "You do not have permission to access this task."

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the task
        """
        return obj.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to all,
    but write access only to the owner
    """

    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        Write permissions only to owner
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
