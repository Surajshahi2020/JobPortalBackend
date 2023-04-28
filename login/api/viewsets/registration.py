from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

from login.api.serializers.registration import (
    StudentCreateSerializer,
    RecruiterCreateSerializer,
)
from django.contrib.auth.models import User
from login.models import StudentUser, Recruiter


@extend_schema_view(
    post=extend_schema(
        description="Student Account Create Api",
        summary="Refer To Schemas At Bottom",
        request=StudentCreateSerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when student is created successfully!",
            ),
            422: OpenApiResponse(
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Registration Apis"],
    ),
)
class StudentAccountCreateView(generics.CreateAPIView):
    queryset = StudentUser.objects.all()
    serializer_class = StudentCreateSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Accounts Create",
                "message": "StudentUser Account Created Successfully!",
                "data": response.data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        description="Recruiter Account Create Api",
        summary="Refer To Schemas At Bottom",
        request=RecruiterCreateSerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when recruiter is created successfully!",
            ),
            422: OpenApiResponse(
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Registration Apis"],
    ),
)
class RecruiterAccountCreateView(generics.CreateAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterCreateSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Accounts Create",
                "message": "Recruiter Account Created Successfully!",
                "data": response.data,
            }
        )
