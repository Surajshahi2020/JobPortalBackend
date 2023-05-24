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
            raise serializers.ValidationError(
                {
                    "title": "Job Post",
                    "message": "User doesnot exist!",
                }
            )
        data["recruiter"] = recruiter.id
        if "image" in data and not validate_image(image):
            raise serializers.ValidationError(
                {
                    "title": "Job Post",
                    "message": "Please enter a valid url for image!",
                }
            )

        if (
            not (start_date and end_date and creationdate)
            or not validate_date_format(start_date)
            or not validate_date_format(end_date)
            or not validate_date_format(creationdate)
        ):
            raise serializers.ValidationError(
                {
                    "title": "Job Post",
                    "message": "Date has wrong format or is not available. Use the format YYYY-MM-DD and ensure the dates are valid.",
                }
            )

        if datetime.strptime(creationdate, "%Y-%m-%d").date() > date.today():
            raise serializers.ValidationError(
                {
                    "title": "Job Post",
                    "message": "Creation date cannot be in the future.",
                }
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
    title = serializers.ReadOnlyField(source="job.title")
    salary = serializers.ReadOnlyField(source="job.salary")
    start_date = serializers.ReadOnlyField(source="job.start_date")
    end_date = serializers.ReadOnlyField(source="job.end_date")
    experience = serializers.ReadOnlyField(source="job.experience")
    creationdate = serializers.ReadOnlyField(source="job.creationdate")
    mobile = serializers.ReadOnlyField(source="student.mobile")
    email = serializers.ReadOnlyField(source="student.user.email")
    first_name = serializers.ReadOnlyField(source="student.user.first_name")
    last_name = serializers.ReadOnlyField(source="student.user.last_name")

    class Meta:
        model = Apply
        fields = [
            "apply_date",
            "resume",
            "title",
            "salary",
            "mobile",
            "email",
            "first_name",
            "last_name",
            "start_date",
            "end_date",
            "creationdate",
            "experience",
        ]


class RecruiterProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
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
            "first_name",
            "last_name",
        ]

    def to_representation(self, instance):
        d = self.initial_data
        user = self.context["request"].user
        user.first_name = d.get("first_name", user.first_name)
        user.last_name = d.get("last_name", user.last_name)
        user.save()
        response = super().to_representation(instance)
        response["first_name"] = user.first_name
        response["last_name"] = user.last_name
        return response

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
        user = instance.user
        validated_data.pop("first_name", user.first_name)
        validated_data.pop("last_name", user.last_name)
        user.save()
        email = validated_data.get("email")
        instance.user.email = email
        instance.user.username = email
        instance.user.save()
        return super().update(instance, validated_data)
