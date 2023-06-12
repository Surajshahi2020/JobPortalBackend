from django.urls import path
from cart.api.viewsets.cart import (
    CartActionView,
    CartGetView,
)


urlpatterns = [
    path("add/", CartActionView.as_view()),
    path("list/", CartGetView.as_view()),
]
