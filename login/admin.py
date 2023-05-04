from django.contrib import admin
from login.models import StudentUser, Recruiter, Job, Apply
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
