from django.urls import path, include

from recruiter.api.viewsets.add_job import (
    JobPostCreateView,
)


urlpatterns = [
    path("job-post/", JobPostCreateView.as_view()),
]
