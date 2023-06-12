from django.contrib import admin
from chat.models import (
    ChatRoom,
    ChatMessage,
)

# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
