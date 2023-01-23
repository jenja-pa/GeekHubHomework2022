from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class AddProductToBasketForm(forms.Form):
    product_pk = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        label="Кількість",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(20)
        ])


class ProductIdForm(forms.Form):
    product_pk = forms.IntegerField(widget=forms.HiddenInput())
