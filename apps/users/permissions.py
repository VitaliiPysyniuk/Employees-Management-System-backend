from rest_framework.permissions import BasePermission

from .models import CustomUserModel


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == CustomUserModel.Role.ADMINISTRATOR)


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == CustomUserModel.Role.EMPLOYEE)
