from rest_framework import serializers
from cart.models import CartItem, UserCart
from login.models import Job
from django.contrib.auth.models import User


class CartActionSerializer(serializers.ModelSerializer):
    product = serializers.CharField(write_only=True, required=False)
    quantity = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data

        if "product" not in data:
            raise serializers.ValidationError(
                {
                    "title": "Cart",
                    "message": "Product Is Required!",
                }
            )
        if "quantity" not in data:
            raise serializers.ValidationError(
                {
                    "title": "Cart",
                    "message": "Quantity Is Required!",
                }
            )

        if data["quantity"] < 0:
            raise serializers.ValidationError(
                {
                    "title": "Cart",
                    "message": "Quantity Is Positive Integer!",
                }
            )

        if not Job.objects.filter(pk=data["product"]).exists():
            raise serializers.ValidationError(
                {
                    "title": "Cart",
                    "message": "Product doesnot exist!",
                }
            )

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        product = validated_data.pop("product")
        quantity = validated_data.pop("quantity")

        user: User = self.context["request"].user

        product = Job.objects.get(pk=product)
        user_cart = UserCart.objects.filter(creator=user)
        if not user_cart.exists():
            user_cart = UserCart.objects.create(creator=user)
        else:
            user_cart = user_cart.first()

        cart_item = CartItem.objects.filter(product=product, creator=user)
        if cart_item.exists():
            if quantity == 0:
                cart_item.delete()
                if user_cart.items.count() == 0:
                    user_cart.delete()
            else:
                cart_item.update(quantity=quantity)
        else:
            if quantity == 0:
                if user_cart.items.count() == 0:
                    user_cart.delete()
            else:
                cart_item = CartItem.objects.create(
                    product=product, quantity=quantity, creator=user
                )
                user_cart.items.add(cart_item)

        return user_cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        exclude = []
        depth = 2
