from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Product


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


class ProductEditForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        # fields = [
        #     'item_id',
        #     'title',
        #     'sell_status',
        #     'old_price',
        #     'current_price',
        #     'href',
        #     'brand',
        #     'category',
        #     'url_image_preview',
        #     'url_image_big',
        # ]
        # widgets = {
        #     'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        # }
        # labels = {
        #     'name': _('Writer'),
        # }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }
        # field_classes = {
        #     'slug': MySlugFormField,
        # }
