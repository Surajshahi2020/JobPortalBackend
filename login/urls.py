# from django.urls import path, include
from django.urls import path, include
from login.api.viewsets.registration import (
    StudentAccountCreateView,
    RecruiterAccountCreateView,
    AdminViewSet,
)
from login.api.viewsets.login import (
    StudentLoginView,
    CustomTokenRefreshView,
    RecruiterLoginView,
    AdminloginViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register("admin-create", AdminViewSet, basename="admin_viewset")
router.register("admin-login", AdminloginViewSet, basename="adminlogin_viewset")


urlpatterns = [
    path("", include(router.urls)),
    path("student-create/", StudentAccountCreateView.as_view()),
    path("recruiter-create/", RecruiterAccountCreateView.as_view()),
    path("student-login/", StudentLoginView.as_view()),
    path("refresh-create/", CustomTokenRefreshView.as_view()),
    path("recruiter-login/", RecruiterLoginView.as_view()),
]
