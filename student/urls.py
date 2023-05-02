from django.urls import path, include

from student.api.viewsets.change_profile import (
    ChangeProfileView,
    StudentPasswordView,
)


urlpatterns = [
    path("change-profile/<int:pk>/", ChangeProfileView.as_view()),
    path("change-password/", StudentPasswordView.as_view()),
]
