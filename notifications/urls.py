from django.urls import path, include
from notifications.api.viewsets.fcm_token import (
    FcmTokenCreateView,
)
from notifications.api.viewsets.notifications import (
    mark_all_notifications_as_read,
    mark_notification_as_read,
    NotificationListView,
)

urlpatterns = [
    path("create", FcmTokenCreateView.as_view(), name="fcm-token"),
    path("", NotificationListView.as_view()),
    path("mark-all-notifications-as-read/", mark_all_notifications_as_read),
    path("mark_notification_as_read/<str:pk>/", mark_notification_as_read),
]
