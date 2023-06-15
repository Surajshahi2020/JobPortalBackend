from django.db import models
from common.models import CommonInfo
from login.models import Job


class Comments(CommonInfo):
    job = models.ForeignKey(Job, on_delete=models.PROTECT, related_name="comments")
    body = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True
    )
    is_published = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"""Comment for {self.job.title}"""

    class Meta:
        ordering = ["-created_at"]
