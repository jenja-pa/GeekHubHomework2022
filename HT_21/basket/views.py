from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from django.forms import model_to_dict as form_to_dict
from django.contrib import messages
from scrapper.forms import AddProductToBasketForm, ProductIdForm
from scrapper.models import Product


MAX_COUNT_ITEM_PRODUCT_IN_BASKET = 20


# Create your views here.
def view_basket(request):
    # request.session.flush()
    basket = request.session.setdefault('basket', {})
    basket_err_modifyed = request.session.setdefault('basket_err_modifyed', {})
    context = {"products_in_basket": {}}
    if basket:
        products = Product.objects.filter(id__in=basket.keys())
        products_in_basket = [model_to_dict(product) for product in products]

        for product in products_in_basket:
            sproduct_id = str(product["id"])
            # if isinstance(basket[sproduct_id], dict):
            #     continue
            product["quantity"] = int(basket[sproduct_id])
            product["form"] = AddProductToBasketForm({
                "product_pk": product["id"],
                "quantity": basket_err_modifyed.get(sproduct_id, basket[sproduct_id]),
                })
            if 'basket_err_modifyed' in request.session.keys():
                del request.session['basket_err_modifyed']

            product["form_delete_product"] = ProductIdForm(
                {'product_pk': product["id"]}
                )
        # Count full cost
        full_cost = sum([
            item['current_price'] * item["quantity"]
            for item in products_in_basket
            ])

        context = {
            "products_in_basket": products_in_basket,
            "full_cost": full_cost,
        }
        request.session.save()        
    return render(request, 'basket/index.html', context=context)


@require_http_methods(["POST"])
def add_to_basket(request):
    form = AddProductToBasketForm(request.POST)
    # entered_quatity = request.POST["quantity"]
    if not form.is_valid():
        # Некоректні дані були введені при
        # додаванні в корзину
        # проводимо redirect на сторінку де
        # вони були введені, в сесії передаємо
        # введені значення, щоб предметно
        # звучало повідомлення про помилку
        form_values = {}
        request.session["form_add_values"] = request.POST
        request.session.save()

        messages.error(request, f"Помилка. Ви спробували додати в корзину {form['quantity'].value()} товарів", extra_tags="basket")

        return redirect(reverse(
            'scrapper:product_detail',
            kwargs={'pk': request.POST['product_pk']}
            ))
    data = form.cleaned_data
    str_pk = str(data['product_pk'])
    basket = request.session.setdefault('basket', {})
    basket.setdefault(str_pk, 0)
    if basket[str(data['product_pk'])] + data["quantity"] > MAX_COUNT_ITEM_PRODUCT_IN_BASKET:
        basket[str(data['product_pk'])] = MAX_COUNT_ITEM_PRODUCT_IN_BASKET
        messages.error(request, f"Увага кількість окремої позиції товару в корзині не повинна перевищувати {MAX_COUNT_ITEM_PRODUCT_IN_BASKET} одиниць", extra_tags="basket")
    else:
        basket[str(data['product_pk'])] += data["quantity"]
    request.session.save()
    return redirect(reverse(
        'scrapper:product_detail',
        kwargs={'pk': data["product_pk"]}
        ))


@require_http_methods(["POST"])
def change_basket_quatity(request):
    form = AddProductToBasketForm(request.POST)
    basket = request.session.setdefault('basket', {})
    if form.is_valid():
        data = form.cleaned_data
        str_pk = str(data['product_pk'])
        basket.setdefault(str_pk, 0)
        basket[str_pk] = data['quantity']
        if 'basket_err_modifyed' in request.session.keys():
            del request.session['basket_err_modifyed']
    else:
        # Дані введені в форму не валідні
        product_pk = form['product_pk'].value()
        basket_err_modifyed = request.session.setdefault('basket_err_modifyed', {})
        basket_err_modifyed.setdefault(product_pk, 0)
        basket_err_modifyed[str(product_pk)] = form['quantity'].value()
        messages.error(request, f"Зміна кількості товару на {form['quantity'].value()}, не можливе. Зміни неможливо провести")

    request.session.save()
    return redirect(reverse('basket:view_basket'))


@require_http_methods(["POST"])
def delete_basket_product(request):
    form = ProductIdForm(request.POST)
    form.is_valid()
    data = form.cleaned_data
    basket = request.session.setdefault('basket', {})
    del basket[str(data['product_pk'])]
    request.session.save()

    return redirect(reverse('basket:view_basket'))


# @require_http_methods(["POST"])
def clear_basket(request):
    request.session.setdefault('basket', {})
    del request.session["basket"]
    request.session.save()

    return redirect(reverse('basket:view_basket'))
