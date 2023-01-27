from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class AddProductToBasketForm(forms.Form):
    product_pk = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        label="Потрібна кількість:",
        validators=[
            MinValueValidator(1, message="Значення не може бути менше 1"),
            MaxValueValidator(20, message="Значення не може бути більше 20")
        ])


class ProductIdForm(forms.Form):
    product_pk = forms.IntegerField(widget=forms.HiddenInput())
