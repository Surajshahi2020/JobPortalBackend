from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from login.api.serializers.registration import (
    RecruiterCreateSerializer,
)

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)


from common.permissions import (
    IsAuthenticated,
)

from recruiter.api.serializers.add_job import (
    JobPostSerializer,
)
from login.models import Job, Recruiter


@extend_schema_view(
    post=extend_schema(
        description="Job Post Api",
        summary="Refer To Schemas At Bottom",
        request=JobPostSerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when Job is created successfully!",
            ),
            422: OpenApiResponse(
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Recruiter Apis"],
    ),
)
class JobPostCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Job Post",
                "message": "Job posted Successfully!",
                "data": response.data,
            }
        )
