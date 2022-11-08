from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Product
from store.serializers import ProductSerializer


@api_view()
def product_list(request):
    queryset = Product.objects.all().order_by("-id")
    products = ProductSerializer(queryset, many=True)
    return Response(products.data)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serialized_product = ProductSerializer(product)
    return Response(serialized_product.data)
