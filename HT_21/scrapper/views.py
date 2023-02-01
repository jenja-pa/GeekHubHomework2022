import re
import threading
import uuid
from pathlib import Path

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import AddProductToBasketForm, ProductEditForm
from .models import Product
from .models import Category
from .models import BackgroundProcessMessage
from .api_rozetka import get_data_from_scraper_and_put_into_db


# Create your views here.
@user_passes_test(lambda user: user.is_superuser, login_url='/')
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
    user = User.objects.first()
    context = {
        "title": "List of scrapered products :: HT_20",
        "products": Product.objects.all(),
        "categories": Category.objects.all(),
        }
    return render(request, 'scrapper/list_products.html', context)


def category_list(request, pk):
    # Вивід продуктів у вказаній категорії
    target_category = Category.objects.get(pk=pk)
    print(f"category_list:{target_category=}")
    context = {
        "title": f"Наявні товари категорії '{target_category.title}' :: HT_21",
        "products": Product.objects.filter(category=target_category),
        }
    print(f"category_list:{context=}")
    return render(request, 'scrapper/list_category_products.html', context)


def product_detail(request, pk):
    basket = request.session.setdefault('basket', {})
    # print(f"product_detail:{basket=} {pk=}")
    product_basket_quantity = basket.get(str(pk))
    # print(f"product_detail:{product_basket_quantity=}")
    storage_messages = messages.get_messages(request)
    product_basket_err_message = ""
    for message in storage_messages:
        if message.level_tag == 'error' and "basket" in message.extra_tags:
            product_basket_err_message = message.message

    context = {
        "title": "List of scrapered products :: HT_20",
        "err_message": request.session.get("err_message"),
        "product": get_object_or_404(Product, pk=pk),
        "product_basket": {
            "quantity": product_basket_quantity,
            "message_err": product_basket_err_message
            },
        'form_add': AddProductToBasketForm(
            initial={'product_pk': pk, "quantity": 1}
            )
    }
    # Якщо відбувся redirect на цю сторінку і з сесії присутні дані форми,
    # що не відповідають обмеженням валідації - (можливо колхоз №2)
    if "form_add_values" in request.session:
        form_add = AddProductToBasketForm(request.session["form_add_values"])
        form_add.is_valid()
        del request.session["form_add_values"]
        request.session.save()
        context["form_add"] = form_add
    # print(f"product_detail:{context=}")
    return render(
        request, 'scrapper/products_detail.html', context)


def product_detail_edit(request, pk):
    print(f"product_detail_edit:{request.method=}, {pk=}")

    context = {
       "title": "Редагування продукта :: HT_21",
       "pk": pk,
    }
    if request.method == "GET":
        context["form"] = ProductEditForm(instance=Product.objects.get(pk=pk)) 
    else:
        # POST need save modified data Product
        form = ProductEditForm(request.POST, instance=Product.objects.get(pk=pk))
        print(f"product_detail_edit:{request.POST=}")
        if form.is_valid():
            print(f"product_detail_edit:valid:{form.cleaned_data=}")
            form.save(commit=True)
            return redirect(reverse("scrapper:product_detail", kwargs={'pk': context["pk"]}))
        else:
            context["form"] = form 
    return render(
        request, 'scrapper/products_detail_edit.html', context)
