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
    first_name = serializers.CharField(write_only=True)

    last_name = serializers.CharField(write_only=True)

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

    class Meta:
        model = StudentUser
        fields = [
            "image",
            "mobile",
            "gender",
            "type",
            "first_name",
            "last_name",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        queryset = StudentUser.objects.exclude(id=self.instance.id).filter(
            mobile=data.get("mobile")
        )
        if not "first_name" in data:
            pass

        if not "last_name" in data:
            pass

        if not "gender" in data:
            pass
        if not "type" in data:
            pass

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "title": "Student Profile",
                    "message": "Mobile number already linked with another user!",
                }
            )
        if "mobile" in data and not validate_number(data.get("mobile")):
            raise serializers.ValidationError(
                {
                    "title": "Student Profile",
                    "message": "Please enter a valid mobile number!",
                }
            )

        if "image" in data and not validate_image(data.get("image")):
            raise serializers.ValidationError(
                {
                    "title": "Student Profile",
                    "message": "Please enter a valid url for image!",
                },
            )

        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        user = instance.user
        validated_data.pop("first_name", user.first_name)
        validated_data.pop("last_name", user.last_name)
        user.save()

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
                {
                    "title": "Student change-password",
                    "message": "User is not a valid instance of User model!",
                }
            )
        studentuser = StudentUser.objects.filter(user=user).first()
        if not studentuser:
            raise serializers.ValidationError(
                {
                    "title": "Student change-password",
                    "message": "This User does not exist in Student model!",
                }
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
            raise serializers.ValidationError(
                {
                    "title": "Job Apply",
                    "message": "Job and resume fields are required!",
                }
            )

        if not job.exists():
            raise serializers.ValidationError(
                {
                    "title": "Job Apply",
                    "message": "Job does not exist!",
                }
            )

        if not student:
            raise serializers.ValidationError(
                {
                    "title": "Job Apply",
                    "message": "This User does not exist in Student model!",
                }
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


class StudentJobAppySerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="job.title")
    salary = serializers.ReadOnlyField(source="job.salary")
    experience = serializers.ReadOnlyField(source="job.experience")
    start_date = serializers.ReadOnlyField(source="job.start_date")
    end_date = serializers.ReadOnlyField(source="job.end_date")

    class Meta:
        model = Apply
        fields = [
            "resume",
            "apply_date",
            "title",
            "salary",
            "experience",
            "start_date",
            "end_date",
        ]
