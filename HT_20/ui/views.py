from django.shortcuts import render


# Create your views here.
def index(request):
    return render(
        request,
        'ui/index.html',
        {"title": "Index page :: HT_19", }
    )
