from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.contrib.auth.models import User

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from cadmin.api.serializers.view_user import (
    AdminSerializer,
    StudentListSerializer,
    RecruiterListSerializer,
)

from common.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from login.models import StudentUser, Recruiter


class AdminListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminSerializer
    pagination_class = CustomPagination
    http_method_names = [
        "get",
        "delete",
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["email"]
    search_fields = ["email"]
    ordering_fields = ["date_joined"]

    @extend_schema(
        description="UserList Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: AdminSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Admin Apis"],
    )
    def list(self, request, *args, **kwargs):
        user_count = User.objects.all().count()
        admin_count = User.objects.filter(
            is_staff=True, is_active=True, is_superuser=True
        ).count()
        student_count = StudentUser.objects.all().count()
        recruiter_count = Recruiter.objects.all().count()
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Admin List",
                "message": "List Fetched successfully !",
                "total_user": user_count,
                "total_admin": admin_count,
                "total_student": student_count,
                "total_recruiter": recruiter_count,
                "data": response.data,
            }
        )

    @extend_schema(
        description="UserList Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: AdminSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Admin Apis"],
        exclude=True,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="UserDelete Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: AdminSerializer,
            404: {
                "message": "Bad Request",
            },
        },
        tags=["Admin Apis"],
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "title": "Student Delete",
                "message": "User deleted successfully!",
            },
            status=200,
        )


@extend_schema_view(
    get=extend_schema(
        description="StudentList Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: OpenApiResponse(
                description="Success Response when user is created successfully!",
            ),
            401: OpenApiResponse(
                description="Authentication error!",
            ),
        },
        tags=["Admin Apis"],
    ),
)
class StudentListView(generics.ListAPIView):
    queryset = StudentUser.objects.all()
    serializer_class = StudentListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["mobile"]

    def list(self, request, *args, **kwargs):
        student_count = StudentUser.objects.all().count()
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Student List",
                "message": "List Fetched Successfully!",
                "total_student": student_count,
                "data": response.data,
            }
        )


@extend_schema(
    description="UserDelete Api",
    summary="Refer to Schemas At Bottom",
    responses={
        200: StudentListSerializer,
        404: {
            "message": "Bad Request",
        },
    },
    tags=["Admin Apis"],
)
class StudentDeleteView(generics.DestroyAPIView):
    queryset = StudentUser.objects.all()
    serializer_class = StudentListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "title": "Student Delete",
                "message": "User deleted successfully!",
            },
            status=200,
        )


@extend_schema_view(
    get=extend_schema(
        description="My Account Get Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: OpenApiResponse(
                description="Success Response when Recruiter is listed successfully!",
            ),
            401: OpenApiResponse(
                description="Authentication error!",
            ),
        },
        tags=["Admin Apis"],
    ),
)
class RecruiterListView(generics.ListAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["mobile"]

    def list(self, request, *args, **kwargs):
        recruiter_count = Recruiter.objects.all().count()
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Recruiter List",
                "message": "List Fetched Successfully!",
                "total_recruiter": recruiter_count,
                "data": response.data,
            }
        )


@extend_schema(
    description="UserDelete Api",
    summary="Refer to Schemas At Bottom",
    responses={
        200: RecruiterListSerializer,
        404: {
            "message": "Bad Request",
        },
    },
    tags=["Admin Apis"],
)
class RecruiterDeleteView(generics.DestroyAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "title": "Recruiter  Delete",
                "message": "Recruiter deleted successfully!",
            },
            status=200,
        )
