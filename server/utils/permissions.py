from rest_framework.permissions import BasePermission


class IsLogin(BasePermission):
    """Rights only for Login"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated)


class IsSellerRole(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='seller').exists()