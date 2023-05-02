from django.urls import path, include

from student.api.viewsets.change_profile import (
    ChangeProfileView,
)


urlpatterns = [
    path("change-profile/<int:pk>/", ChangeProfileView.as_view()),
]
