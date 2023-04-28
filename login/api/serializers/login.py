from rest_framework import serializers
from login.api.serializers.registration import BaseUserCreateSerializer
from login.models import StudentUser


class LoginSerializer(BaseUserCreateSerializer):
    class Meta:
        model = StudentUser
        fields = [
            "email",
            "password",
        ]
