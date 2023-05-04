from rest_framework import viewsets
from miscellaneous.api.serializers.informative import InfoPageSerializer
from miscellaneous.models import InfoPage
from common.permissions import *
from common.pagination import CustomPagination
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework.response import Response


class InfoPageViewset(viewsets.ModelViewSet):
    queryset = InfoPage.objects.all()
    serializer_class = InfoPageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    http_method_names = [
        "get",
        "post",
    ]

    @extend_schema(
        summary="Refer To Schemas At Bottom",
        request=InfoPageSerializer,
        responses={200: InfoPageSerializer, 404: {"message": "Bad Request"}},
        tags=["Informative s"],
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Info list",
                "message": "Info list listed successfully!",
                "data": response.data,
            }
        )

    @extend_schema(
        summary="Refer To Schemas At Bottom",
        request=InfoPageSerializer,
        responses={200: InfoPageSerializer, 404: {"message": "Bad Request"}},
        tags=["Informative s"],
    )
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            {
                "title": "Info page",
                "message": "Info page retrieved successfully!",
                "data": response.data,
            }
        )

    @extend_schema(
        summary="Refer To Schemas At Bottom",
        examples=[
            OpenApiExample(
                name="About Us - Ab",
                request_only=True,
                value={
                    "title": "Ab",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Privacy and Policy - Pr",
                request_only=True,
                value={
                    "title": "Te",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Terms and Conditions - Te",
                request_only=True,
                value={
                    "title": "Te",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Contact - Co",
                request_only=True,
                value={
                    "title": "Co",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Navigation Bar - Na",
                request_only=True,
                value={
                    "title": "Na",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Navigation Logo - Nl",
                request_only=True,
                value={
                    "title": "Nl",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Location - Lc",
                request_only=True,
                value={
                    "title": "Lc",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Social account - So",
                request_only=True,
                value={
                    "title": "So",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="FAQ / Help - Fa",
                request_only=True,
                value={
                    "title": "Fa",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Footer content - Fo",
                request_only=True,
                value={
                    "title": "Fo",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Footer content - Fo",
                request_only=True,
                value={
                    "title": "Fo",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Footer logo - Fg",
                request_only=True,
                value={
                    "title": "Fo",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Browse Job Logo",
                request_only=True,
                value={
                    "title": "Br",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Notice",
                request_only=True,
                value={
                    "title": "No",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Extra 1",
                request_only=True,
                value={
                    "title": "E1",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Extra 2",
                request_only=True,
                value={
                    "title": "E2",
                    "content": {
                        "description": "string",
                    },
                },
            ),
            OpenApiExample(
                name="Extra 3",
                request_only=True,
                value={
                    "title": "E3",
                    "content": {
                        "description": "string",
                    },
                },
            ),
        ],
        responses={200: {}, 422: {"message": "Bad Request"}},
        tags=["Informative s"],
    )
    def create(self, request, *args, **kwargs):
        return Response(
            {
                "title": "Info page created",
                "message": "Info page created successfully!",
                "data": super().create(request, *args, **kwargs).data,
            }
        )
