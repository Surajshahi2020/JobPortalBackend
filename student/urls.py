from django.urls import path, include

from student.api.viewsets.change_profile import (
    ChangeProfileView,
    StudentPasswordView,
    JobApplyView,
)


urlpatterns = [
    path("change-profile/<int:pk>/", ChangeProfileView.as_view()),
    path("change-password/", StudentPasswordView.as_view()),
    path("job-apply/", JobApplyView.as_view()),
]
