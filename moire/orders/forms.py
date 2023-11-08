from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "name",
            "address",
            "phone",
            "email",
            "comment",
            "delivery",
            "paid_variant",
        ]
