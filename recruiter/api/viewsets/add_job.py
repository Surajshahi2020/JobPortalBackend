from rest_framework import generics, viewsets
from rest_framework.response import Response

from login.api.serializers.registration import (
    RecruiterCreateSerializer,
)

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

from recruiter.api.serializers.add_job import (
    RecruiterPasswordSerializer,
    CandidateListSerializer,
    RecruiterProfileSerializer,
)


from common.permissions import (
    IsAuthenticated,
    IsRecruiter,
    IsStudent,
    method_permission_classes,
)
from common.pagination import CustomPagination

from recruiter.api.serializers.add_job import (
    JobPostSerializer,
)
from login.models import Job, Recruiter, Apply
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


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


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter()
    serializer_class = JobPostSerializer
    pagination_class = CustomPagination
    http_method_names = [
        "get",
        "delete",
        "patch",
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "recruiter"]
    search_fields = ["experience"]
    ordering_fields = ["creationdate"]

    @extend_schema(
        description="JobList Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: JobPostSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Recruiter Apis"],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "title": "Job List",
                "message": "Job listed successfully",
                "data": serializer.data,
                # "jobtitle": seria
            },
            200,
        )

    @extend_schema(
        description="JobList Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: JobPostSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Recruiter Apis"],
        exclude=True,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="JobDelete Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: JobPostSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Recruiter Apis"],
    )
    @method_permission_classes([IsRecruiter])
    def destroy(self, request, *args, **kwargs):
        job_id = kwargs.get("pk")
        recruiter = Job.objects.filter(id=job_id).first()
        if not recruiter:
            return Response(
                {
                    "title": "Job Delete",
                    "message": "Job does not exist!",
                },
                200,
            )
        super().destroy(request, *args, **kwargs)
        return Response(
            {
                "title": "Job Delete",
                "message": "Job Deleted Successfully",
            },
            200,
        )

    @extend_schema(
        description="JobPatch Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: JobPostSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Recruiter Apis"],
    )
    @method_permission_classes([IsRecruiter])
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "title": "Job Update",
                "message": "Job updated successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        description="Change Password Api",
        summary="Refer to Schemas At Bottom",
        request=RecruiterPasswordSerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when password is changed successfully!",
            ),
            401: OpenApiResponse(
                description="Authentication error!",
            ),
        },
        tags=["Recruiter Apis"],
    ),
)
class RecruiterPasswordView(generics.CreateAPIView):
    serializer_class = RecruiterPasswordSerializer
    permission_classes = [IsRecruiter]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Recruiter change-password",
                "message": "Recruiter password changed successfully!",
            }
        )


@extend_schema_view(
    get=extend_schema(
        description="Candidate-Applied List Api",
        summary="Refer to Schemas At Bottom",
        request=CandidateListSerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when list  is fetched successfully!",
            ),
            401: OpenApiResponse(
                description="Authentication error!",
            ),
        },
        tags=["Recruiter Apis"],
    ),
)
class CandidateListView(generics.ListAPIView):
    queryset = Apply.objects.filter()
    serializer_class = CandidateListSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["job"]
    search_fields = ["experience"]

    @method_permission_classes([IsRecruiter])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(
            job__recruiter__user=request.user
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "title": "Candidates List",
                "message": "Candidates listed successfully",
                "data": serializer.data,
            },
            200,
        )


@extend_schema_view(
    patch=extend_schema(
        description="RecruiterProfile Api",
        summary="Refer to Schemas At Bottom",
        responses={
            200: OpenApiResponse(
                description="Success Response when profile is changed successfully!",
            ),
            401: OpenApiResponse(
                description="Authentication error!",
            ),
        },
        tags=["Recruiter Apis"],
    ),
)
class RecruiterProfileView(generics.UpdateAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterProfileSerializer
    permission_classes = [IsRecruiter]
    http_method_names = [
        "patch",
    ]

    def update(self, request, *args, **kwargs):
        if not Recruiter.objects.filter(id=kwargs.get("pk")).exists():
            return Response(
                {
                    "title": "Profile update",
                    "messaage": "Recruiter doesnot exist!",
                }
            )
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "title": "Recruiter Profile",
                "message": "Profie changed successfully",
                "data": response.data,
            }
        )
