from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from common.models import CommonInfo
from common.utils import DEVICE_TYPES, SOUND_CHOICES, NOTIF_PRIORITY


class FCMTokenObject(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    device_id = models.CharField(blank=True, null=True, db_index=True, max_length=255)
    registration_id = models.TextField(null=False, blank=False)
    type = models.CharField(choices=DEVICE_TYPES, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.type}--{self.user}--{self.active}"


class UserNotification(CommonInfo):
    to = models.ForeignKey(
        FCMTokenObject, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.TextField(null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    image = models.URLField()
    sound = models.CharField(default="default", choices=SOUND_CHOICES, max_length=255)
    android_channel_id = models.CharField(default="chimeki", max_length=255)
    data = models.JSONField(default=dict)
    priority = models.CharField(
        default="high", choices=NOTIF_PRIORITY, max_length=255, null=False, blank=False
    )
    is_sent = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.to}--{self.is_sent}"
