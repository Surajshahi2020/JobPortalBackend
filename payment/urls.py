from payment.api.viewsets.payment import (
    KhaltiPaymentCreateView,
    KhaltiPaymentVerifyCreateView,
)


from django.urls import path, include


urlpatterns = [
    path("make-payment/", KhaltiPaymentCreateView.as_view()),
    path("verify-payment/", KhaltiPaymentVerifyCreateView.as_view()),
]
