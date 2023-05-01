from django.urls import path, include

from cadmin.api.viewsets.view_user import (
    UserListViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register("user-list", UserListViewSet, basename="userlist_viewset")


urlpatterns = [
    path("", include(router.urls)),
]
