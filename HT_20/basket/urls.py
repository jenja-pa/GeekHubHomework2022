"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.view_basket, name="view_basket"),
    path('add-to-basket', views.add_to_basket, name="add"),
    # path('products/', views.list_products, name="list_products"),
    # path('products/<int:pk>/', views.product_detail, name="product_detail"),
]
