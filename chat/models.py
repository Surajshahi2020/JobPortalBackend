from django.db import models
from uuid import uuid4
from common.utils import MSG_TYPES
from login.models import (
    User,
    Job,
)


class ChatRoom(models.Model):
    room_name = models.CharField(
        unique=True, max_length=255, default=uuid4, null=False, blank=False
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="chat_user",
    )
    products = models.ManyToManyField(
        Job,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return "Room Name - {f}".format(f=self.room_name)


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom, null=False, blank=False, on_delete=models.DO_NOTHING
    )
    message = models.TextField(null=False, blank=False)
    created_for = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=False, blank=False
    )
    seen = models.BooleanField(default=False)
    type = models.CharField(choices=MSG_TYPES, max_length=5, default="TEXT")

    def __str__(self) -> str:
        return "Message - {f} - Type - {g}".format(
            f=self.message[:50],
            g=self.type,
        )
