from rest_framework import generics
from rest_framework.response import Response

from chat.api.serializers.chat_serializer import (
    ChatRoomCreateSerializer,
)

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

from common.serializer import (
    OperationError,
    OperationSuccess,
)

from chat.models import (
    ChatRoom,
)


@extend_schema_view(
    post=extend_schema(
        description="ChatRoom Create Api",
        summary="Refer To Schemas At Bottom",
        request=ChatRoomCreateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when chatroom is created successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["CHAT APIS s"],
    ),
)
class ChatRoomCreateView(generics.CreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomCreateSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "ChatRoom Create",
                "message": "ChatRoom Created Successfully!",
                "data": response.data,
            }
        )
