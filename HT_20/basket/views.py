from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict

from scrapper.forms import AddProductToBasketForm
from scrapper.models import Product


# Create your views here.
def view_basket(request):
    basket = request.session.get('basket')
    products = Product.objects.filter(id__in=basket.keys())

    products_in_basket = [model_to_dict(product) for product in products]
    for product in products_in_basket:
        product["quantity"] = basket[str(product["id"])]
    context = {"products_in_basket": products_in_basket}
    return render(request, 'basket/index.html', context=context)


@require_http_methods(["POST"])
def add_to_basket(request):
    if request.method == "POST":
        form = AddProductToBasketForm(request.POST)
        entered_quatity = request.POST["quantity"]
        if not form.is_valid():
            request.session["err_message"] = f"Помилка. Кількість товару повинна бути 1..20, а не {entered_quatity}"
            request.session.save()
            return redirect(reverse('scrapper:product_detail', kwargs={'pk': request.POST['product_pk']}))
        data = form.cleaned_data
        basket = request.session.setdefault('basket', {})
        basket.setdefault(str(data['product_pk']), 0)
        basket[str(data['product_pk'])] += data["quantity"]
        request.session.save()
        print(f"session:{request.session.items()}")
        return redirect(reverse('scrapper:product_detail', kwargs={'pk': data["product_pk"]}))
    else:
        return redirect(reverse('scrapper:list_products'))
