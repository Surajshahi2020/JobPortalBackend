from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from common.serializer import OperationError, OperationSuccess
from common.permissions import IsAuthenticated, IsStudent, method_permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from comments.models import Comments
from comments.api.serializers.comments import (
    CommentSerializer,
    AddCommentSerializer,
    EditCommentSerializer,
)
from common.pagination import CustomPagination

from common.utils import validate_uuid
from rest_framework import serializers
from django.contrib.auth.models import User


class CommentListViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.filter(parent__isnull=True)
    pagination_class = CustomPagination
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer
        elif self.request.method == "POST":
            return AddCommentSerializer
        else:
            return EditCommentSerializer

    @extend_schema(
        description="Comments List Api",
        summary="Refer To Schemas At Bottom",
        request=CommentSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when comments list are retrieved successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Comments Apis"],
    )
    @method_permission_classes((IsAuthenticated,))
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
                "title": "Comments",
                "message": "Comments listed successfully.",
                "data": serializer.data,
            }
        )

    @extend_schema(
        description="Comment Retrieve Api",
        summary="Refer To Schemas At Bottom",
        request=CommentSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when a comment is retrieved successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Comments Apis"],
    )
    @method_permission_classes((IsAuthenticated,))
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            {
                "title": "Comments",
                "message": "Comment retrieved successfully.",
                "data": response.data,
            }
        )

    @extend_schema(
        description="Add comment Api",
        summary="Refer To Schemas At Bottom",
        request=AddCommentSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when comment is added successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Comments Apis"],
    )
    @method_permission_classes((IsStudent,))
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Comment",
                "message": "Comment added successfully.",
                "data": response.data,
            }
        )

    @extend_schema(
        description="Edit comment Api",
        summary="Refer to Schemans at bottom",
        request=EditCommentSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when comment is deleted successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Comments Apis"],
    )
    @method_permission_classes((IsStudent,))
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "title": "Comment",
                "message": "Comment added successfully.",
                "data": response.data,
            }
        )

    @extend_schema(
        description="Delete Comment Api",
        summary="Refer To Schemas At Bottom",
        request=None,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when comment is deleted successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Comments Apis"],
    )
    @method_permission_classes((IsAuthenticated,))
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            {
                "title": "Comments",
                "message": "Commment Deleted successfully",
            }
        )
