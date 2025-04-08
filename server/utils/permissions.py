from rest_framework.permissions import BasePermission


class IsLogin(BasePermission):
    """Rights only for Login"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated)