from django.db import models
import time
from django.dispatch import receiver
from django.db.models.signals import pre_save
from common.utils import TitleFieldSlug, PANEL_CHOICES


def upload_handler(obj, file_path):
    file_name = str(time.time()).replace(".", "")
    return f"{obj.directory}/{file_name}.{file_path.split('.')[-1]}"


# Create your models here.
class CommonImage(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=upload_handler, null=False, blank=False)
    directory = models.CharField(max_length=45, default="common")

    def __str__(self) -> str:
        return f"{self.image.url} - {self.directory}"


class InfoPage(models.Model):
    title = models.CharField(max_length=3, choices=PANEL_CHOICES, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.JSONField(default=dict)
    is_published = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title[:3]}..."


@receiver(pre_save, sender=InfoPage)
def infoPageSave(sender, instance: InfoPage, *args, **kwargs):
    if not instance.slug:
        instance.slug = TitleFieldSlug(instance)
