from django.urls import path, include

from recruiter.api.viewsets.add_job import (
    JobPostCreateView,
    JobViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()


router.register("job-list", JobViewSet, basename="joblist_viewset")


urlpatterns = [
    path("", include(router.urls)),
    path("job-post/", JobPostCreateView.as_view()),
]
