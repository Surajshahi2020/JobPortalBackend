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


class StudentListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email

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
