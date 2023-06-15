from rest_framework import serializers
from notifications.models import FCMTokenObject
from common.utils import is_valid_choice, DEVICE_TYPES


class FcmTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMTokenObject
        fields = "__all__"
        extra_kwargs = {
            "user": {
                "read_only": True,
            },
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if not "type" in data and not data.get("type"):
            raise serializers.ValidationError(
                {
                    "title": "FCM",
                    "message": "Type is required field!",
                }
            )
        if not "registration_id" in data and not data.get("registration_id"):
            raise serializers.ValidationError(
                {
                    "title": "FCM",
                    "message": "Registration id is required field!",
                }
            )
        if not is_valid_choice(data.get("type"), DEVICE_TYPES):
            raise serializers.ValidationError(
                {
                    "title": "FCM",
                    "message": "Plese select valid choice for Type field!",
                },
            )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = self.context["request"].user
        device_type = validated_data.get("type")
        instance = FCMTokenObject.objects.filter(user=user, type=device_type).first()
        if instance:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        return FCMTokenObject.objects.create(**validated_data, user=user)
