from django.contrib import admin

from .models import Product
from .models import BackgroundProcessMessage

# Register your models here.
admin.site.register(Product)
admin.site.register(BackgroundProcessMessage)
