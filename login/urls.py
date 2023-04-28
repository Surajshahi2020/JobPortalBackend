# from django.urls import path, include
from django.urls import path, include
from login.api.viewsets.registration import (
    StudentAccountCreateView,
    RecruiterAccountCreateView,
)
from rest_framework import routers

urlpatterns = [
    path("student-create/", StudentAccountCreateView.as_view()),
    path("recruiter-create/", RecruiterAccountCreateView.as_view()),
]
