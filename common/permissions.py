from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import exceptions


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
