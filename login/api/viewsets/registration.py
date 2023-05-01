from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
import threading

from login.api.serializers.registration import (
    StudentCreateSerializer,
    RecruiterCreateSerializer,
    AdminCreateSerializer,
)
from django.contrib.auth.models import User
from login.models import StudentUser, Recruiter
from common.mail_sender import send_mail_function


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


class AdminCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminCreateSerializer

    http_method_names = [
        "post",
    ]

    @extend_schema(
        description="Admin login Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: AdminCreateSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Registration Apis"],
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dat = serializer.create(serializer.validated_data)
        dat = self.get_serializer(dat).data
        threading.Thread(
            target=send_mail_function,
            daemon=True,
            args=(
                data.get("email"),
                {
                    "data": {
                        **dat,
                        "id": dat.get("email"),
                        "password": data.get("password"),
                    },
                    "message": "Account created successfully",
                    "title": "Account Created,Job Portal ",
                },
            ),
        ).start()
        return Response(
            {
                "title": "Admin Login",
                "message": "Admin created Successfully",
            }
        )
