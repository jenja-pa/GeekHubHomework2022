from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from django.forms import model_to_dict as form_to_dict
from django.contrib import messages
from scrapper.forms import AddProductToBasketForm, ProductIdForm
from scrapper.models import Product


# Create your views here.
def view_basket(request):
    basket = request.session.get('basket')
    print(f"{basket=}")
    context = {"products_in_basket": {}}
    if basket:
        products = Product.objects.filter(id__in=basket.keys())
        products_in_basket = [model_to_dict(product) for product in products]
        for product in products_in_basket:
            product["quantity"] = int(basket[str(product["id"])]["quantity"])
            print(f"{basket[str(product['id'])].keys()=}")
            product["form"] = AddProductToBasketForm({
                "product_pk": product["id"], 
                "quantity": 1 if "new_quantity" not in basket[str(product["id"])].keys() else int(basket[str(product["id"])]["new_quantity"]),
                })
            # product["form"].is_valid()

            product["form_delete_product"] = ProductIdForm(
                initial={'product_pk': product["id"]}
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
    return render(request, 'basket/index.html', context=context)


@require_http_methods(["POST"])
def add_to_basket(request):
    form = AddProductToBasketForm(request.POST)
    entered_quatity = request.POST["quantity"]
    if not form.is_valid():
        # Це мій колхоз №2 - по redirect некоректних даних 
        # на сторінку де воно були введені
        form_values = {}
        for name_field in form.declared_fields:
            form_values[name_field] = form[name_field].value()
        request.session["form_add_values"] = form_values
        request.session.save()
        return redirect(reverse(
            'scrapper:product_detail',
            kwargs={'pk': request.POST['product_pk']}
            ))
    data = form.cleaned_data
    basket = request.session.setdefault('basket', {})
    basket.setdefault(str(data['product_pk']), {})
    print(f"{basket[str(data['product_pk'])]=}")
    if not basket[str(data['product_pk'])]:
        basket[str(data['product_pk'])]['quantity'] = 0
    print(f"{basket[str(data['product_pk'])]=}")
    basket[str(data['product_pk'])]['quantity'] += data["quantity"]
    print(f"{basket[str(data['product_pk'])]=}")
    request.session.save()
    return redirect(reverse(
        'scrapper:product_detail',
        kwargs={'pk': data["product_pk"]}
        ))


@require_http_methods(["POST"])
def change_basket_quatity(request):
    form = AddProductToBasketForm(request.POST)
    form.is_valid()
    data = form.cleaned_data
    basket = request.session.setdefault('basket', {})
    basket[str(data['product_pk'])] = dict(
        new_quantity=int(form['quantity'].value()),
        quantity=int(basket[str(data['product_pk'])]['quantity'])
        )
    request.session.save()

    # if form.is_valid():
    #     data = form.cleaned_data
    #     basket = request.session.setdefault('basket', {})
    #     basket[str(data['product_pk'])] = data["quantity"]
    #     request.session.save()
    # else:
    #     print(f"FORM not VALID: quantity:{request.POST['quantity']}"
    #           f" is not valid")

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


@require_http_methods(["POST"])
def clear_basket(request):
    request.session.setdefault('basket', {})
    del request.session["basket"]
    request.session.save()

    return redirect(reverse('basket:view_basket'))
