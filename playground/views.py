from django.shortcuts import render
from store.models import Product, Customer
from django.db.models import F, Value, Q, Func
from django.db.models.functions import Concat


def hello(request):

    # products = Product.objects.values_list("title", "collection__title")
    # products = Product.objects.select_related("collection").all()
    products = Product.objects.select_related("collection").all()

    # customers = Customer.objects.annotate(full_name=Func(F("first_name"), Value(" "), F("last_name"), function="CONCAT"))
    customers = Customer.objects.annotate(
        full_name=Concat("first_name", Value(" "), "last_name")
    )
    customers = list(customers)

    return render(request, "hello.html", {"products": list(products)})
