from django.shortcuts import render

from shop.models import Product


# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/home.html', context)


def view(request):
    context =  {'product_details': product}
    return render(request, 'shop/product_view.html', context)
