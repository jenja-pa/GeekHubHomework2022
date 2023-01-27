import re
import threading
import uuid
from pathlib import Path

from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .forms import AddProductToBasketForm
from .models import Product
from .models import BackgroundProcessMessage
from .api_rozetka import get_data_from_scraper_and_put_into_db


# Create your views here.
def scrape_outer_data(request):
    context = {
        "title": "Scraper page :: HT_20",
        # "helper_messages": [],
    }

    if request.method == "POST":
        str_need_ids = request.POST["list_ids"]
        lst_ids = re.split(r"[\s,;]+", str_need_ids.strip())
        # get information about list_ids from scrapper
        if lst_ids and lst_ids[0] != '':
            # Present ids to load - run thread
            name_thread = f"Scrapper_Thread-{str(uuid.uuid4())[:6]}"
            thread = threading.Thread(
                target=get_data_from_scraper_and_put_into_db,
                name=name_thread,
                args=(lst_ids, name_thread),
                daemon=None)
            thread.start()
    else:
        # Get method - first enter
        messages.info(
            request,
            (Path(Path.cwd()) / "scrapper" / "templates" / "scrapper" /
                "start_ids_rozetka.txt").read_text(encoding="utf-8")
        )

    # Вибір останніх 10 продуктів із БД
    last_ten_products = Product.objects.all().order_by('-id')[:10]
    products = reversed(last_ten_products)
    context["products"] = products

    proceses = []
    for thread in threading.enumerate():
        if thread.name.startswith("Scrapper_Thread-"):
            proceses.append(thread)
    context["proceses"] = proceses

    # Prepare helper message
    bg_messages_model = BackgroundProcessMessage.objects.all()
    if bg_messages_model:
        for bg_message_model in bg_messages_model:
            messages.info(
                request,
                f"{bg_message_model.value}"
            )
            bg_message_model.delete()

    return render(request, 'scrapper/scrape_data.html', context)


def list_products(request):
    context = {
        "title": "List of scrapered products :: HT_20",
        "products": Product.objects.all(),
        }
    return render(request, 'scrapper/list_products.html', context)


def product_detail(request, pk):
    context = {
        "title": "List of scrapered products :: HT_20",
        "err_message": request.session.get("err_message"),
        "product": get_object_or_404(Product, pk=pk),
        'form': AddProductToBasketForm(
            initial={'product_pk': pk, "quantity": 1}
            )
    }
    print(f"product_detail: {request.method=}")
    if request.method == 'POST':
        form = AddProductToBasketForm(request.POST)
        context["form"] = form

    request.session["err_message"] = None
    request.session.save()
    return render(
        request, 'scrapper/products_detail.html', context)
