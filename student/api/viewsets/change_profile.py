from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

from student.api.serializers.change_profile import (
    StudentProfileSerializer,
    StudentPasswordSerializer,
    JobApplySerializer,
)

from common.permissions import (
    IsStudent,
)

from login.models import StudentUser


@extend_schema_view(
    patch=extend_schema(
        description="StudentProfile Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: OpenApiResponse(
                description="Success Response when profile is changed successfully!",
            ),
            401: OpenApiResponse(
                description="Authentication error!",
            ),
        },
        tags=["Student Apis"],
    ),
)
class ChangeProfileView(generics.UpdateAPIView):
    queryset = StudentUser.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsStudent]
    http_method_names = [
        "patch",
    ]

    def update(self, request, *args, **kwargs):
        if not StudentUser.objects.filter(id=kwargs.get("pk")).exists():
            return Response(
                {
                    "title": "Profile update",
                    "messaage": "StudentUser doesnot exist!",
                }
            )
        return super().update(request, *args, **kwargs)


@extend_schema_view(
    post=extend_schema(
        description="Change Password Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: OpenApiResponse(
                description="Success Response when password is changed successfully!",
            ),
            401: OpenApiResponse(
                description="Authentication error!",
            ),
        },
        tags=["Student Apis"],
    ),
)
class StudentPasswordView(generics.CreateAPIView):
    serializer_class = StudentPasswordSerializer
    permission_classes = [IsStudent]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Student change-password",
                "message": "Student password changed successfully!",
            }
        )


@extend_schema_view(
    post=extend_schema(
        description="Job Apply Api",
        summary="Refer to Schemas At Bottom",
        request=JobApplySerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when job applied successfully!",
            ),
            401: OpenApiResponse(
                description="Authentication error!",
            ),
        },
        tags=["Student Apis"],
    ),
)
class JobApplyView(generics.CreateAPIView):
    serializer_class = JobApplySerializer
    permission_classes = [IsStudent]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Job Apply",
                "message": "Job Applied Successfully!",
                "data": response.data,
            }
        )
