from django.db import models
from catalog.models import Item


class Order(models.Model):
    class Delivery(models.TextChoices):
        SELF_DELIVERY = "SD"
        COURIER = "CO"

    class PaidVariant(models.TextChoices):
        CARD = "CARD"
        CASH = "CASH"

    name = models.CharField(max_length=200, verbose_name="ФИО")
    address = models.CharField(max_length=250, verbose_name="Адрес")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    comment = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Комментарий"
    )
    delivery = models.CharField(
        max_length=150,
        choices=Delivery.choices,
        default=Delivery.SELF_DELIVERY,
        verbose_name="Способ доставки",
    )
    paid_variant = models.CharField(
        max_length=150,
        choices=PaidVariant.choices,
        default=PaidVariant.CARD,
        verbose_name="Способ оплаты",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Item, related_name="order_item", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
