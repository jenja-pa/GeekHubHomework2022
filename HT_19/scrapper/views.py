import re

from django.shortcuts import render

from .models import Products
from .api_rozetka import get_data_from_scraper_and_put_into_db

# Create your views here.
def index(request):
    if request.method == "POST":
        str_need_ids = request.POST["list_ids"]
        lst_ids = re.split(r"[\s,;]+", str_need_ids)
        print(f"{str_need_ids=}")
        print(f"{lst_ids=}")

        # get information about list_ids from scrapper
        get_data_from_scraper_and_put_into_db(lst_ids)

    products = Products.objects.all()
    return render(
        request,
        'scrapper/index.html',
        {
            "products": products,
            "title": "index page project django scrapper :: HT_19"
        }
    )
