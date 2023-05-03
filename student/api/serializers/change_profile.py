from rest_framework import serializers
from login.models import StudentUser, Apply, Job
from django.contrib.auth.models import User
from datetime import date
from cadmin.api.serializers.view_user import (
    BaseChangePasswordSerializer,
)

from common.utils import (
    validate_number,
    validate_image,
    validate_resume,
)
from django.db.models import Q


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentUser
        fields = [
            "image",
            "mobile",
            "gender",
            "type",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        queryset = StudentUser.objects.exclude(id=self.instance.id)
        mobile_user = queryset.filter(Q(mobile=data.get("mobile")))
        if mobile_user.exists():
            raise serializers.ValidationError(
                "Mobile number already linked with another user!",
            )
        if "mobile" in data and not validate_number(data.get("mobile")):
            raise serializers.ValidationError("Please enter a valid mobile number!")

        if "image" in data and not validate_image(data.get("image")):
            raise serializers.ValidationError("Please enter a valid url for image!")

        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class StudentPasswordSerializer(BaseChangePasswordSerializer):
    class Meta:
        model = StudentUser
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
        studentuser = StudentUser.objects.filter(user=user).first()
        if not studentuser:
            raise serializers.ValidationError(
                "This User does not exist in Student model!"
            )
        return super().is_valid(raise_exception=raise_exception)


class JobApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = [
            "resume",
            "job",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        user = self.context["request"].user
        student = StudentUser.objects.get(user=user)
        job_id = data.get("job")
        resume = data.get("resume")
        job = Job.objects.filter(id=job_id)
        validate_resume(resume)

        if not all([data.get("job"), data.get("resume")]):
            raise serializers.ValidationError("Job and resume fields are required!")

        if not job.exists():
            raise serializers.ValidationError("Job does not exist!")

        if not student:
            raise serializers.ValidationError(
                "This User does not exist in Student model!"
            )

        if Apply.objects.filter(job=job_id, student=student).exists():
            raise serializers.ValidationError(
                {
                    "title": " Job Apply",
                    "message": "You have already applied for this job.",
                }
            )

        super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = self.context["request"].user
        student = StudentUser.objects.get(user=user)
        job_id = validated_data.get("job")

        return Apply.objects.create(
            **validated_data, student=student, apply_date=date.today()
        )
