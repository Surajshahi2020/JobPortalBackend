from cart.api.serializers.cart import (
    CartActionSerializer,
    CartSerializer,
)
from rest_framework import generics
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)
from cart.models import CartItem, UserCart
from common.pagination import CustomPagination
from common.permissions import IsAuthenticated


@extend_schema_view(
    post=extend_schema(
        tags=["Cart[User]"],
        description="User Cart Add Remove Api - Add 0 To Remove And >0 qty to add/increase quantity of item in cart!",
        summary="User Cart Add / Remove Api",
    )
)
class CartActionView(generics.CreateAPIView):
    queryset = UserCart.objects.all()
    serializer_class = CartActionSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(
            {
                "title": "Cart",
                "message": "Cart Updated Successfully!",
                "data": super().create(request, *args, **kwargs).data,
            }
        )


@extend_schema_view(
    get=extend_schema(
        tags=["Cart[User]"],
        description="User Cart Get",
        summary="User Cart Get Api",
    )
)
class CartGetView(generics.GenericAPIView):
    queryset = UserCart.objects.all()
    serializer_class = CartSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        cart = UserCart.objects.filter(creator=user)
        if cart.exists():
            cart = cart.first()
            ser = self.get_serializer(cart, many=False).data
            return Response(
                {
                    "title": "Cart",
                    "message": "Cart Fetched Successfully!",
                    "data": ser,
                }
            )
        else:
            return Response(
                {
                    "title": "Cart",
                    "message": "Your cart is empty, please add some items in it!",
                    "data": {},
                }
            )
