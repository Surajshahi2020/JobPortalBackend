from django.contrib import admin
from login.models import StudentUser, Recruiter, Job, Apply

# Register your models here.
admin.site.register(StudentUser)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Apply)
