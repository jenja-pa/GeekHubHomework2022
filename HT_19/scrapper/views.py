from django.shortcuts import render

from .models import Products


# Create your views here.
def index(request):
    products = Products.objects.all()
    return render(
        request,
        'scrapper/index.html',
        {
            "products": products,
            "title": "index page project django scrapper :: HT_19"
        }
    )
