from rest_framework import serializers
from chat.models import (
    ChatMessage,
    ChatRoom,
)
from login.models import Job


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), many=False, write_only=True
    )

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "product",
            "products",
            "seller",
        ]
        extra_kwargs = {
            "products": {
                "read_only": True,
            },
            "seller": {
                "read_only": True,
            },
        }
