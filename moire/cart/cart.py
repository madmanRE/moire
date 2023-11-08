from decimal import Decimal
from django.conf import settings
from catalog.models import Item


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item, quantity=1, override_quantity=False):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {"quantity": 0, "price": str(item.price)}
        if override_quantity:
            self.cart[item_id]["quantity"] = quantity
        else:
            self.cart[item_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            if len(self.cart) == 0:
                self.cart.clear()
            self.save()

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        cart = self.cart.copy()
        for item in items:
            cart[str(item.id)]["item"] = item
        for i in cart.values():
            i["price"] = Decimal(i["price"])
            i["total_price"] = i["price"] * i["quantity"]
            yield i

    def __len__(self):
        return sum(i["quantity"] for i in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(i["price"]) * i["quantity"] for i in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
