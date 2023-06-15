from django.urls import path, include
from rest_framework.routers import DefaultRouter
from comments.api.viewsets.comments import CommentListViewSet

router = DefaultRouter()
router.register("job-comment", CommentListViewSet, basename="reviews_admin")

urlpatterns = [
    path("", include(router.urls)),
]
