from django.urls import path, include

from cadmin.api.viewsets.view_user import (
    AdminListViewSet,
    StudentListView,
    RecruiterListView,
    StudentDeleteView,
    RecruiterDeleteView,
    ChangeStatusView,
    RecruiterPendingView,
    RecruiterAcceptedView,
    RecruiterRejectedView,
    ChangePasswordView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register("admin-list", AdminListViewSet, basename="adminlist_viewset")


urlpatterns = [
    path("", include(router.urls)),
    path("student-list/", StudentListView.as_view()),
    path("recruiter-list/", RecruiterListView.as_view()),
    path("student-delete/<int:pk>/", StudentDeleteView.as_view()),
    path("recruiter-delete/<int:pk>/", RecruiterDeleteView.as_view()),
    path("change-status/<int:pk>/", ChangeStatusView.as_view()),
    path("pending-list/", RecruiterPendingView.as_view()),
    path("acccepted-list/", RecruiterAcceptedView.as_view()),
    path("rejected-list/", RecruiterRejectedView.as_view()),
    path("change-password/<int:pk>/", ChangePasswordView.as_view()),
]
