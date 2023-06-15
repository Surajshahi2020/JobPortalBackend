from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from rest_framework import generics
from common.serializer import (
    OperationSuccess,
    OperationError,
)
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from notifications.api.serializers.notifications import NotificationSerializer
from common.permissions import IsAuthenticated
from common.pagination import CustomPagination
from notifications.models import UserNotification
from common.utils import validate_uuid


@extend_schema_view(
    get=extend_schema(
        description="Notifications List Api",
        summary="Refer To Schemas At Bottom",
        request=NotificationSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when notifications list is retrieved successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Notifications Apis"],
    ),
)
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        self.queryset = UserNotification.objects.filter(creator=self.request.user)
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Notifications List",
                "message": "Notifications list retreived successfully.",
                **response.data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        description="Mark All Notifications As Read Api",
        summary="Refer To Schemas At Bottom",
        request=None,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when all notifications are marked as read successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Notifications Apis"],
    ),
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_all_notifications_as_read(request):
    UserNotification.objects.filter(creator=request.user, is_read=False).update(
        is_read=True
    )
    return Response(
        {
            "title": "Notifications",
            "message": "All notifications marked as read.",
        }
    )


@extend_schema_view(
    post=extend_schema(
        description="Mark A Notification As Read Api",
        summary="Refer To Schemas At Bottom",
        request=None,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when a notification is marked as read successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Notifications Apis"],
    ),
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, pk):
    if not validate_uuid(pk):
        raise serializers.ValidationError(
            {
                "title": "Notifications",
                "message": "Invalid UUID!",
            }
        )
    notification = UserNotification.objects.filter(creator=request.user, id=pk).first()
    if not notification:
        raise serializers.ValidationError(
            {
                "title": "Notifications",
                "message": "Not found!",
            }
        )
    notification.update(is_read=True)
    return Response(
        {
            "title": "Notifications",
            "message": "Notification marked as read.",
        }
    )
