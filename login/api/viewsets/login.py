from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError


from django.contrib.auth.models import User


from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

from login.api.serializers.login import (
    LoginSerializer,
)
from login.models import StudentUser
import datetime


@extend_schema_view(
    post=extend_schema(
        description="Login Api",
        summary="Email Login Api",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when user is loggedin successfully!",
            ),
            422: OpenApiResponse(
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Login Apis"],
    ),
)
class StudentLoginView(generics.CreateAPIView):
    queryset = StudentUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(email=data.get("email")).first()
        if user:
            student = StudentUser.objects.filter(user=user)
            if student:
                student: StudentUser = student.first()
                if student.is_blocked:
                    return Response(
                        {
                            "title": "Account Login",
                            "message": "Account Blocked !",
                        },
                        status=401,
                    )
                if user.check_password(data.get("password")):
                    refresh = RefreshToken.for_user(student)
                    refresh.set_exp(lifetime=datetime.timedelta(days=14))
                    access = refresh.access_token
                    access.set_exp(lifetime=datetime.timedelta(days=1))
                    return Response(
                        {
                            "title": "Account Login",
                            "message": "Logged in successfully !",
                            "data": {
                                "mobile": student.mobile,
                                "gender": student.gender,
                                "slug": student.slug,
                                "type": student.type,
                                "is_blocked": student.is_blocked,
                                "Joined date": student.user.date_joined,
                                "is_active": student.user.is_active,
                                "access": f"{access}",
                                "refresh": f"{refresh}",
                            },
                        }
                    )
                else:
                    return Response(
                        {
                            "title": "Login",
                            "message": "Password incorrect !",
                        },
                        status=422,
                    )

            else:
                return Response(
                    {
                        "title": "Login",
                        "message": "StudentUser does not exist!",
                    },
                    status=422,
                )
        else:
            return Response(
                {
                    "title": "Login",
                    "message": "Email does not linked with user!",
                },
                status=422,
            )


@extend_schema_view(
    post=extend_schema(
        description="Account Refresh Api",
        summary="Refresh Token Api",
        responses={
            200: OpenApiResponse(
                description="Success Response when token refreshed successfully!",
            ),
            422: OpenApiResponse(
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Login Apis"],
    ),
)
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response(
                {
                    "title": "Login",
                    "message": "Email does not linked with user!",
                },
                status=422,
            )

        return Response(
            {
                "title": "Login Refresh",
                "message": "Login Refreshed Successfully!",
                "data": serializer.validated_data,
            },
            status=200,
        )
