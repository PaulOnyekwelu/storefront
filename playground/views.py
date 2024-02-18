from django.shortcuts import render
from store.models import Product


def hello(request):
    products = Product.objects.all()

    return render(request, "hello.html", {"result": list(products)})

