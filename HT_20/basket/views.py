from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict

from scrapper.forms import AddProductToBasketForm, ProductIdForm
from scrapper.models import Product


# Create your views here.
def view_basket(request):
    basket = request.session.get('basket')
    context = {"products_in_basket": {}}
    if basket:
        products = Product.objects.filter(id__in=basket.keys())
        products_in_basket = [model_to_dict(product) for product in products]
        for product in products_in_basket:
            product["quantity"] = basket[str(product["id"])]
            product["form"] = AddProductToBasketForm(initial={'product_pk': product["id"], "quantity": product["quantity"]})
            product["form_delete_product"] = ProductIdForm(initial={'product_pk': product["id"]})

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
    if request.method == "POST":
        form = AddProductToBasketForm(request.POST)
        entered_quatity = request.POST["quantity"]
        if not form.is_valid():
            request.session["err_message"] = f"Помилка. Кількість товару повинна бути 1..20, а не {entered_quatity}"
            request.session.save()
            return redirect(reverse(
                'scrapper:product_detail',
                kwargs={'pk': request.POST['product_pk']}
                ))
        data = form.cleaned_data
        basket = request.session.setdefault('basket', {})
        basket.setdefault(str(data['product_pk']), 0)
        basket[str(data['product_pk'])] += data["quantity"]
        request.session.save()
        return redirect(reverse(
            'scrapper:product_detail',
            kwargs={'pk': data["product_pk"]}
            ))
    else:
        return redirect(reverse('scrapper:list_products'))


@require_http_methods(["POST"])
def change_basket_quatity(request):
    if request.method == "POST":
        form = AddProductToBasketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            basket = request.session.setdefault('basket', {})
            basket[str(data['product_pk'])] = data["quantity"]
            request.session.save()
        else:
            print(f"FORM not VALID: quantity:{request.POST['quantity']} is not valid")
        # print(f"session:{request.session.items()}")

    return redirect(reverse('basket:view_basket'))


@require_http_methods(["POST"])
def delete_basket_product(request):
    if request.method == "POST":
        form = ProductIdForm(request.POST)
        form.is_valid()
        data = form.cleaned_data
        basket = request.session.setdefault('basket', {})
        del basket[str(data['product_pk'])]
        request.session.save()

    return redirect(reverse('basket:view_basket'))


@require_http_methods(["POST"])
def clear_basket(request):
    print("---===================")
    print(f"clear_basket: {request=}")
    if request.method == "POST":
        pass

    return redirect(reverse('basket:view_basket'))
