import re
import threading

from django.shortcuts import render, get_object_or_404

from .models import Product
from .models import BackgroundProcessMessage

from .api_rozetka import get_data_from_scraper_and_put_into_db


# Create your views here.
def index(request):
    return render(
        request,
        'scrapper/index.html',
        {"title": "Index page :: HT_19", }
    )


def scrape_outer_data(request):
    helper_messages = []
    if request.method == "POST":
        str_need_ids = request.POST["list_ids"]
        lst_ids = re.split(r"[\s,;]+", str_need_ids)

        # get information about list_ids from scrapper
        if lst_ids and lst_ids[0] != '':
            # Present ids to load - run thread
            thread = threading.Thread(
                target=get_data_from_scraper_and_put_into_db,
                name=None,
                args=(lst_ids, ),
                daemon=None)
            thread.start()
            ident = thread.ident
            thread.name = f"My_Thread-{ident}"
    else:
        # Get method - first enter
        helper_messages = ["""
Коди для тестового завантаження продуктів:
27714809, 336517495 172762346 316707118 285500098 Wrong8585 102222222
356899741 4333544 25113785 31127199 330748390 333974350 36913984
208273399 292853758"""]

    # Вибір останніх 10 продуктів із БД
    last_ten_products = Product.objects.all().order_by('-id')[:10]
    products = reversed(last_ten_products)

    proceses = []
    for thread in threading.enumerate():
        # print(f"{thread.name=} {thread.daemon=}")
        if thread.name.startswith("My_Thread-"):
            proceses.append(thread)
    # Prepare helper message
    bg_messages = BackgroundProcessMessage.objects.all()
    if bg_messages:
        helper_messages.append(
            "Закінчено фонові процеси:")
        for bg_message in bg_messages:
            helper_messages.append(bg_message.value)
            bg_message.delete()

    return render(
        request,
        'scrapper/scrape_data.html',
        {
            "title": "Scraper page :: HT_19",
            "products": products,
            "proceses": proceses,
            "helper_messages": helper_messages,
        }
    )


def list_products(request):
    products = Product.objects.all()
    return render(
        request,
        'scrapper/list_products.html',
        {
            "title": "List of scrapered products :: HT_19",
            "products": products,
        }
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(
        request,
        'scrapper/products_detail.html',
        {
            "title": "Detail data - product :: HT_19",
            "product": product,
        }
    )
