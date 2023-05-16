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
    StudentJobAppySerializer,
)

from common.permissions import (
    IsStudent,
)

from common.pagination import CustomPagination


from login.models import StudentUser, Apply
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


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
                    "title": "Student Profile",
                    "messaage": "StudentUser doesnot exist!",
                }
            )
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "title": "Student Profile",
                "message": "Student profile updated successfully",
                "data": response.data,
            }
        )


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
        data = request.data
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Student change-password",
                "message": "Student password changed successfully!",
                "data": response.data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        description="Job Apply Post Api",
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


@extend_schema_view(
    get=extend_schema(
        description="Job Apply List Api",
        summary="Refer to Schemas At Bottom",
        request=JobApplySerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when job applied list is listed successfully!",
            ),
            401: OpenApiResponse(
                description="Authentication error!",
            ),
        },
        tags=["Student Apis"],
    ),
)
class JobApplyListView(generics.ListAPIView):
    queryset = Apply.objects.all()
    serializer_class = StudentJobAppySerializer
    permission_classes = [IsStudent]
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["apply_date"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(
            student__user=request.user
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "title": "Student Applied Job",
                "message": "Applied Job listed successfully",
                "data": serializer.data,
            },
            200,
        )
