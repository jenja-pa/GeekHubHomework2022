import re

from django.shortcuts import render, get_object_or_404

from .models import Product
from .api_rozetka import get_data_from_scraper_and_put_into_db

# Create your views here.
def index(request):
    if request.method == "POST":
        str_need_ids = request.POST["list_ids"]
        lst_ids = re.split(r"[\s,;]+", str_need_ids)

        # get information about list_ids from scrapper
        get_data_from_scraper_and_put_into_db(lst_ids)

    products = Product.objects.all()
    if len(products) > 0:
        print(f"{products[0].old_price=}")
    return render(
        request,
        'scrapper/index.html',
        {
            "products": products,
            "title": "index page project django scrapper :: HT_19"
        }
    )

def list_products(request):
    products = Product.objects.all()
    return render(
        request,
        'scrapper/list_products.html',
        {
            "products": products,
            "title": "list of scrapered products :: HT_19"
        }
    )

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(
        request,
        'scrapper/products_detail.html',
        {
            "product": product,
            "title": "Detail data for product :: HT_19"
        }
    )
