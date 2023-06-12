from django.db import models

from django.db.models import Sum, F

from common.models import CommonInfo
from login.models import Job


class CartItem(CommonInfo):
    quantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Job, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.quantity} -- {self.creator}"


class UserCart(CommonInfo):
    items = models.ManyToManyField(CartItem, blank=True)

    @property
    def total_price(self):
        tp = (
            self.items.all()
            .aggregate(
                total=Sum(
                    F("product__price") * F("quantity"),
                )
            )
            .get("total")
        )
        return tp

    def __str__(self) -> str:
        return f"{self.total_price}--{self.creator}"

    class Meta:
        ordering = ["-created_at"]
