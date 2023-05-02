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
)

from common.permissions import (
    IsAuthenticated,
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
    permission_classes = [IsAuthenticated]
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
