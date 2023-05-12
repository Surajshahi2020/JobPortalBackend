from rest_framework import serializers
from login.api.serializers.registration import BaseUserCreateSerializer
from login.models import StudentUser, Recruiter
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
        ]


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


class AdminLogginSerializer(BaseUserCreateSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]
