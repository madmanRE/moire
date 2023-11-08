from .models import Category, Item
from django.db.models import Count
from cart.cart import Cart


def categories(request):
    data = {"categories": Category.objects.all()}
    return data


def filter_counts(request):
    filter_quantity = {
        "LN": Item.objects.filter(material="LN").count(),
        "CT": Item.objects.filter(material="CT").count(),
        "WL": Item.objects.filter(material="WL").count(),
        "SL": Item.objects.filter(material="SL").count(),
        "SM": Item.objects.filter(collection="SM").count(),
        "WN": Item.objects.filter(collection="WN").count(),
        "AU": Item.objects.filter(collection="AU").count(),
        "SP": Item.objects.filter(collection="SP").count(),
    }
    return {"filter_quantity": filter_quantity}


def cart_count(request):
    cart = Cart(request)
    return {"total_quantity": len(cart)}
