from django.contrib import admin
from notifications.models import (
    FCMTokenObject,
    UserNotification,
)

# Register your models here.
admin.site.register([FCMTokenObject, UserNotification])
