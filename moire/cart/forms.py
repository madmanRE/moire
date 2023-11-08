from django import forms


class CartAddItemForm(forms.Form):
    quantity = forms.IntegerField()
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
