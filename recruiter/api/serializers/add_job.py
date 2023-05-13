from rest_framework import serializers
from login.models import Job, Recruiter, Apply
from common.utils import validate_image, validate_date_format, validate_number
from datetime import datetime, date
from django.contrib.auth.models import User
from cadmin.api.serializers.view_user import (
    BaseChangePasswordSerializer,
)


class JobPostSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    def get_company(self, obj: Job):
        if obj.recruiter:
            return obj.recruiter.company
        return ""

    class Meta:
        model = Job
        exclude = [
            "slug",
            "recruiter",
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


class CandidateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = "__all__"


class RecruiterProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)

    class Meta:
        model = Recruiter
        fields = [
            "image",
            "mobile",
            "gender",
            "type",
            "company",
            "email",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        email = data.get("email")
        mobile = Recruiter.objects.exclude(id=self.instance.id).filter(
            mobile=data.get("mobile")
        )
        if mobile.exists():
            raise serializers.ValidationError(
                {
                    "title": "Recriter Profile",
                    "message": "Mobile number already linked with another user!",
                }
            )
        if User.objects.exclude(id=self.instance.user.id).filter(email=email).exists():
            raise serializers.ValidationError(
                {
                    "title": "Recruiter Profile",
                    "message": "Email already exists",
                }
            )
        if "mobile" in data and not validate_number(data.get("mobile")):
            raise serializers.ValidationError(
                {
                    "title": "Recruiter Profile",
                    "message": "Please enter a valid mobile number!",
                },
            )

        if "image" in data and not validate_image(data.get("image")):
            raise serializers.ValidationError(
                {
                    "title": "Recruiter Profile",
                    "message": "Please enter a valid url for image!",
                },
            )

        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        email = validated_data.get("email")
        instance.user.email = email
        instance.user.username = email
        instance.user.save()
        return super().update(instance, validated_data)
