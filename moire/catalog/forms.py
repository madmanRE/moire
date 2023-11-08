from django import forms
from .models import *


class FilterForm(forms.Form):
    min_price = forms.DecimalField(min_value=0, max_value=9999999999, required=False)
    max_price = forms.DecimalField(min_value=0, max_value=9999999999, required=False)
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберете категорию",
        required=False,
    )
    material = forms.CharField(max_length=250, required=False)
    collection = forms.CharField(max_length=250, required=False)
