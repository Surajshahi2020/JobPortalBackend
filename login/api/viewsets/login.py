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
    RecruiterLoginSerializer,
    AdminLogginSerializer,
    UserSerializer,
)

from login.models import (
    StudentUser,
    Recruiter,
)
import datetime


@extend_schema_view(
    post=extend_schema(
        description="Student Login Api",
        summary="Refer to Schemas At Bottom",
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
                if student.type == "student":
                    if student.is_blocked:
                        return Response(
                            {
                                "title": "Student Login",
                                "message": "Student Account Blocked !",
                            },
                            status=401,
                        )
                    if user.check_password(data.get("password")):
                        refresh = RefreshToken.for_user(student.user)
                        refresh.set_exp(lifetime=datetime.timedelta(days=14))
                        access = refresh.access_token
                        access.set_exp(lifetime=datetime.timedelta(days=1))
                        return Response(
                            {
                                "title": "Student Login",
                                "message": "Student Logged in successfully !",
                                "data": {
                                    "mobile": student.mobile,
                                    "gender": student.gender,
                                    "slug": student.slug,
                                    "type": student.type,
                                    "is_blocked": student.is_blocked,
                                    "access": f"{access}",
                                    "refresh": f"{refresh}",
                                    "own_id": student.id,
                                    "image": student.image.url,
                                    **UserSerializer(student.user).data,
                                },
                            }
                        )
                    return Response(
                        {
                            "title": "Student Login",
                            "message": "Student Password incorrect !",
                        },
                        status=422,
                    )
                return Response(
                    {
                        "title": "Student Login",
                        "message": "Invalid User !",
                    },
                    status=422,
                )

            return Response(
                {
                    "title": "Student Login",
                    "message": "Email does not linked with student model!!",
                },
                status=422,
            )
        return Response(
            {
                "title": "Student Login",
                "message": "Email does not linked with user model!",
            },
            status=422,
        )


@extend_schema_view(
    post=extend_schema(
        description="Account Refresh Api",
        summary="Refer to Schemas At Bottom",
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


@extend_schema_view(
    post=extend_schema(
        description="Recruiter Login Api",
        summary="Refer to Schemas At Bottom",
        request=RecruiterLoginSerializer,
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
class RecruiterLoginView(generics.CreateAPIView):
    queryset = StudentUser.objects.all()
    serializer_class = RecruiterLoginSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(email=data.get("email")).first()
        if user:
            recruiter = Recruiter.objects.filter(user=user)
            if recruiter:
                recruiter: Recruiter = recruiter.first()
                if recruiter.type == "recruiter":
                    if recruiter.is_blocked:
                        return Response(
                            {
                                "title": "Recruiter Login",
                                "message": "Recriter Account Blocked !",
                            },
                            status=401,
                        )

                    if recruiter.status == "accepted":
                        if user.check_password(data.get("password")):
                            refresh = RefreshToken.for_user(recruiter.user)
                            refresh.set_exp(lifetime=datetime.timedelta(days=14))
                            access = refresh.access_token
                            access.set_exp(lifetime=datetime.timedelta(days=1))
                            joined_date = recruiter.user.date_joined
                            return Response(
                                {
                                    "title": "Recruiter Login",
                                    "message": "Recruiter Logged in successfully !",
                                    "data": {
                                        "mobile": recruiter.mobile,
                                        "gender": recruiter.gender,
                                        "slug": recruiter.slug,
                                        "type": recruiter.type,
                                        "company": recruiter.company,
                                        "is_blocked": recruiter.is_blocked,
                                        "status": recruiter.status,
                                        "joined date": joined_date.strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        ),
                                        "own_id": recruiter.id,
                                        "image": recruiter.image.url,
                                        "access": f"{access}",
                                        "refresh": f"{refresh}",
                                        **UserSerializer(recruiter.user).data,
                                    },
                                }
                            )
                        return Response(
                            {
                                "title": "Recruiter Login",
                                "message": "Recruiter Incorrect password !",
                            },
                            status=422,
                        )
                    return Response(
                        {
                            "title": "Recruiter Login",
                            "message": "Recruiter account is in Pending !",
                        },
                        status=422,
                    )
                return Response(
                    {
                        "title": "Recruiter Login",
                        "message": "Only Recruiter can login!",
                    },
                    status=422,
                )

            else:
                return Response(
                    {
                        "title": "Recruiter Login",
                        "message": "Email doesnot linked with Recruiter model!!",
                    },
                    status=422,
                )
        else:
            return Response(
                {
                    "title": "Recruiter Login",
                    "message": "Email does not linked with user model!",
                },
                status=422,
            )


class AdminloginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminLogginSerializer
    http_method_names = [
        "post",
    ]

    @extend_schema(
        description="Admin login Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: AdminLogginSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Login Apis"],
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(email=data.get("email"))
        if user:
            user: User = user.first()
            if user.is_staff and user.is_active and user.is_superuser:
                if user.check_password(data.get("password")):
                    refresh = RefreshToken.for_user(user)
                    refresh.set_exp(lifetime=datetime.timedelta(days=14))
                    access = refresh.access_token
                    access.set_exp(lifetime=datetime.timedelta(days=1))
                    joined_date = user.date_joined

                    return Response(
                        {
                            "title": "Admin Login",
                            "message": "AdminLogged in successfully !",
                            "data": {
                                "email": user.email,
                                "joined_date": joined_date.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "is_staff": user.is_staff,
                                "is_active": user.is_active,
                                "is_superuser": user.is_superuser,
                                "access": f"{access}",
                                "refresh": f"{refresh}",
                            },
                        },
                    )
                return Response(
                    {
                        "title": "Admin Login",
                        "message": "Incorrect Password!!",
                    }
                )
            return Response(
                {
                    "title": "Admin Login",
                    "message": "Not activated!!",
                }
            )
        else:
            return Response(
                {
                    "title": "Admin Login",
                    "message": "Email doesnot linked with user!",
                }
            )
