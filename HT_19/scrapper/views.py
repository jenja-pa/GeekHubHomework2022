import re
import threading

from django.shortcuts import render, get_object_or_404

from .models import Product
from .api_rozetka import get_data_from_scraper_and_put_into_db

# Create your views here.
def index(request):
    return render(
        request,
        'scrapper/index.html',
        {
            "title": "Index page django scrapper :: HT_19"
        }
    )


def scrape_outer_data(request):
    if request.method == "POST":
        str_need_ids = request.POST["list_ids"]
        lst_ids = re.split(r"[\s,;]+", str_need_ids)

        # get information about list_ids from scrapper
        print(f"scrape_outer_data {lst_ids=}")
        if lst_ids and lst_ids[0] != '':
            # Present ids to load - run thread
            thread = threading.Thread(
                target=get_data_from_scraper_and_put_into_db, 
                name=None, 
                args=(lst_ids, ), 
                daemon=None)
            thread.start()
            ident = thread.ident
            # print(f"My_Thread-{ident}")
            # print("---->", dir(thread))
            thread.name=f"My_Thread-{ident}"

    # products = Product.objects.all()
    # Вибір останніх 10 продуктів із БД
    last_ten_products = Product.objects.all().order_by('-id')[:10]
    products = reversed(last_ten_products)

    proceses = []
    for thread in threading.enumerate():
        # print(f"{thread.name=} {thread.daemon=}")
        if thread.name.startswith("My_Thread-") :
            proceses.append(thread)

    return render(
        request,
        'scrapper/scrape_data.html',
        {
            "products": products,
            "proceses": proceses,
            "title": "Scraper page django scrapper :: HT_19"
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
