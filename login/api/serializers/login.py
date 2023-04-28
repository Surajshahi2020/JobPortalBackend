from rest_framework import serializers
from login.api.serializers.registration import BaseUserCreateSerializer
from login.models import StudentUser, Recruiter
from django.contrib.auth.models import User


class LoginSerializer(BaseUserCreateSerializer):
    class Meta:
        model = StudentUser
        fields = [
            "email",
            "password",
        ]


class RecruiterLoginSerializer(BaseUserCreateSerializer):
    class Meta:
        model = Recruiter
        fields = [
            "email",
            "password",
        ]
