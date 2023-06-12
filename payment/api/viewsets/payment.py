from rest_framework import generics
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from login.models import Payment
from payment.api.serializers.payment import (
    KhaltiPaymentSerializer,
    KhaltiPaymentVerifySerializer,
)
from common.permissions import IsStudent


@extend_schema_view(
    post=extend_schema(
        description="Khalti Payment Api",
        summary="Refer To Schemas At Bottom",
        request=KhaltiPaymentSerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when payment is  successfully!",
            ),
            422: OpenApiResponse(
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Payment Apis"],
    ),
)
class KhaltiPaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = KhaltiPaymentSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "khalti Payment",
                "message": "Payment Done Successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        description="Khalti Payment verify Api",
        summary="Refer To Schemas At Bottom",
        request=KhaltiPaymentVerifySerializer,
        responses={
            200: OpenApiResponse(
                description="Success Response when payment is  successfully!",
            ),
            422: OpenApiResponse(
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Payment Apis"],
    ),
)
class KhaltiPaymentVerifyCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = KhaltiPaymentVerifySerializer
    permission_classes = [IsStudent]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "khalti Payment",
                "message": "Payment Done Successfully",
                "data": response.data,
            }
        )
