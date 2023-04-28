from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User

from login.models import (
    StudentUser,
    Recruiter,
    Job,
    Apply,
)
from common.utils import validate_number, validate_image
from login.models import StudentUser, Recruiter


class BaseUserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        abstract = True
        extra_kwargs = {
            "email": {
                "required": True,
            },
            "type": {
                "read_only": True,
            },
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        mobile = data.get("mobile")
        image = data.get("image")
        if "email" not in data:
            raise serializers.ValidationError("Email is required!")
        if User.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError("User with this Email already exists !")
        if "mobile" not in data:
            raise serializers.ValidationError("Mobile number is required")
        if not validate_number(mobile):
            raise serializers.ValidationError(" Please enter the valid mobile numbers")
        if "image" in data and not validate_image(image):
            raise serializers.ValidationError("Please enter a valid url for image!")

        return super().is_valid(raise_exception=raise_exception)


class StudentCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = StudentUser
        fields = [
            "email",
            "password",
            "slug",
            "image",
            "mobile",
            "gender",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        user = User(email=email, username=email)
        user.set_password(password)
        user.save()

        return StudentUser.objects.create(user=user, **validated_data, type="student")


class RecruiterCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = Recruiter
        fields = [
            "email",
            "password",
            "slug",
            "image",
            "mobile",
            "gender",
            "company",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        user = User(email=email, username=email)
        user.set_password(password)
        user.save()

        return Recruiter.objects.create(
            user=user, **validated_data, type="recruiter", status="deactivated"
        )
