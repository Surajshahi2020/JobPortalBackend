from rest_framework import serializers
from notifications.models import UserNotification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = "__all__"
