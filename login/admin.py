from django.contrib import admin
from login.models import StudentUser, Recruiter, Job, Apply
from login.models import Payment
from miscellaneous.models import (
    CommonImage,
    InfoPage,
)

# Register your models here.
admin.site.register(StudentUser)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Apply)
admin.site.register(CommonImage)
admin.site.register(InfoPage)
admin.site.register(Payment)
