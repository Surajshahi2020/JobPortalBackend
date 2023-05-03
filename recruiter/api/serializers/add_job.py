from rest_framework import serializers
from login.models import Job, Recruiter
from common.utils import validate_image, validate_date_format
from datetime import datetime, date
from django.contrib.auth.models import User
from cadmin.api.serializers.view_user import (
    BaseChangePasswordSerializer,
)


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = [
            "slug",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        creationdate = data.get("creationdate")
        image = data.get("image")
        user = self.context["request"].user
        recruiter = Recruiter.objects.filter(user=user).first()
        if not recruiter:
            raise serializers.ValidationError("User doesnot exist!")
        data["recruiter"] = recruiter.id
        if "image" in data and not validate_image(image):
            raise serializers.ValidationError("Please enter a valid url for image!")
        if datetime.strptime(creationdate, "%Y-%m-%d").date() > date.today():
            raise serializers.ValidationError("Creation date cannot be in the future.")

        if (
            not validate_date_format(start_date)
            or not validate_date_format(end_date)
            or not validate_date_format(creationdate)
        ):
            raise serializers.ValidationError(
                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
            )

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        recruiter = validated_data.pop("recruiter")
        job = Job.objects.create(recruiter=recruiter, **validated_data)
        return job


class RecruiterPasswordSerializer(BaseChangePasswordSerializer):
    class Meta:
        model = Recruiter
        fields = [
            "old_password",
            "new_password",
            "confirm_password",
        ]

    def is_valid(self, *, raise_exception=False):
        user = self.context["request"].user
        if not isinstance(user, User):
            raise serializers.ValidationError(
                "User is not a valid instance of User model!"
            )
        recruiter = Recruiter.objects.filter(user=user).first()
        if not recruiter:
            raise serializers.ValidationError(
                "This User does not exist in Recruiter model!"
            )
        return super().is_valid(raise_exception=raise_exception)
