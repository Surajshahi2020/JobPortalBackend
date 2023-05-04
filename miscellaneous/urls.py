from miscellaneous.api.viewsets.image import ImageUploadView
from miscellaneous.api.viewsets.informative import InfoPageViewset


from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

router.register("info", InfoPageViewset)


urlpatterns = [
    path("", include(router.urls)),
    path("upload/", ImageUploadView.as_view()),
]
