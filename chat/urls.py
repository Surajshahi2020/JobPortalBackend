from django.urls import include, path
from chat.api.viewsets.chat_serializer import (
    ChatRoomCreateView,
)

urlpatterns = [
    path("initiate/", ChatRoomCreateView.as_view()),
]
