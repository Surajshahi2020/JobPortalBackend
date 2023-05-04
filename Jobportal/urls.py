from django.contrib import admin
from django.urls import path, include


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("db/admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                # Api Documentation
                path("doc/schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "doc/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
                path("accounts/", include("login.urls")),
                path("cadmin/", include("cadmin.urls")),
                path("student/", include("student.urls")),
                path("recruiter/", include("recruiter.urls")),
                path("miscellaneous/", include("miscellaneous.urls")),
            ],
        ),
    ),
]
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Jobportal import settings

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
