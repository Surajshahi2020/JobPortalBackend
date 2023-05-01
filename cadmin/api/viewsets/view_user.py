from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from cadmin.api.serializers.view_user import (
    UserSerializer,
)
from login.models import StudentUser, Recruiter


class UserListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer
    http_method_names = [
        "get",
        "get",
    ]

    @extend_schema(
        description="UserList Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: UserSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Admin Apis"],
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        total_count = User.objects.all().count()
        student = UserSerializer(
            User.objects.filter(
                pk__in=list(
                    map(
                        lambda x: x.get("user"),
                        Recruiter.objects.all().values("user"),
                    )
                )
            ),
            many=True,
        )
        student_count = StudentUser.objects.all().count()
        recruiter = UserSerializer(
            User.objects.filter(
                pk__in=list(
                    map(
                        lambda x: x.get("user"),
                        StudentUser.objects.all().values("user"),
                    )
                )
            ),
            many=True,
        )
        recruiter_count = Recruiter.objects.all().count()
        admin_count = total_count - student_count - recruiter_count
        return Response(
            {
                "title": "User list",
                "message": "User list fetched successfully!",
                "data": {
                    "Admin": response.data,
                    "Recruiter": student.data,
                    "StudentUser": recruiter.data,
                    "total_count": total_count,
                    "admin_count": admin_count,
                    "student_count": student_count,
                    "recruiter_count": recruiter_count,
                },
            }
        )

    @extend_schema(
        description="UserList Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: UserSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Admin Apis"],
        exclude=True,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
