from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import exceptions
from login.models import StudentUser


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_anonymous:
            return True
        raise exceptions.AuthenticationFailed(
            {
                "title": "Unauthenticated",
                "message": "Not authenticated",
            },
            code=401,
        )


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_anonymous:
            if StudentUser.objects.filter(user=user).exists():
                return True
            else:
                raise exceptions.PermissionDenied(
                    {
                        "title": "Permission Denied",
                        "message": "Recruiters are not allowed to perform this action",
                    },
                    code=403,
                )
        raise exceptions.AuthenticationFailed(
            {
                "title": "Unauthenticated",
                "message": "Not authenticated",
            },
            code=422,
        )
