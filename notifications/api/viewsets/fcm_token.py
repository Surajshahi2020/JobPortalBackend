from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from rest_framework import generics
from rest_framework.response import Response
from common.serializer import OperationError, OperationSuccess
from notifications.models import FCMTokenObject
from notifications.api.serializers.fcm_token import FcmTokenSerializer


@extend_schema_view(
    post=extend_schema(
        description="FCM token create api",
        summary="Refer to schemas at bottom",
        request=FcmTokenSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when user FCM Token is created successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Notifications Apis"],
    )
)
class FcmTokenCreateView(generics.CreateAPIView):
    queryset = FCMTokenObject.objects.all()
    serializer_class = FcmTokenSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "FcmToken",
                "message": "Created successfully",
                "data": response.data,
            }
        )
