import signal
from rest_framework import serializers
from django.contrib.auth.models import User
from login.models import StudentUser, Recruiter


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "last_login",
            "date_joined",
        ]


class BaseChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        abstract = True
        fields = [
            "old_password",
            "new_password",
            "confirm_password",
        ]

    def validate(self, attrs):
        user = self.context["request"].user
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        if not user.is_authenticated:
            raise serializers.ValidationError(
                "Authentication credentials were not provided."
            )

        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {
                    "old_password": "Wrong password.",
                },
            )

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match.",
                },
            )

        if old_password == new_password:
            raise serializers.ValidationError(
                {
                    "new_password": "New password cannot be the same as old password.",
                },
            )

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        new_password = validated_data["new_password"]
        user.set_password(new_password)
        user.save()

        return user


class ChangePasswordSerializer(BaseChangePasswordSerializer):
    class Meta:
        model = User
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
        if (
            StudentUser.objects.filter(user=user).exists()
            or Recruiter.objects.filter(user=user).exists()
        ):
            raise serializers.ValidationError("This User does not exist in User model!")
        return super().is_valid(raise_exception=raise_exception)


class StudentListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    class Meta:
        model = StudentUser

        fields = "__all__"


class RecruiterListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Recruiter

        fields = "__all__"
