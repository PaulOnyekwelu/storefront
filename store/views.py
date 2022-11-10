from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from store.models import Product, Collection, OrderItem
from store.serializers import ProductSerializer, CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(pk=kwargs['pk']).count() > 0:
            return Response(
                {
                    "message": "unable to delete product"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count("products")
    ).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection__id=kwargs['pk']).count() > 0:
            return Response(
                {"message": "Unable to delete collection linked to product"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


class ProductList(ListCreateAPIView):
    """
    Endpoint: store/products
    Methods: GET, POST, OPTIONS
    """
    queryset = Product.objects.select_related(
        "collection").all().order_by("-id")
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    """
    Endpoint: store/products/<int:id>
    Methods: GET, PUT, DELETE, OPTIONS
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response(
                {
                    "message": "unable to delete product"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        product.delete()
        return Response({"status": True}, status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    """
    Endpoint: store/collection/
    Methods: GET, POST, OPTIONS
    """
    queryset = Collection.objects.annotate(
        products_count=Count("products")
    ).all().order_by("pk")
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    """
    Endpoint: store/collection/<int:id>
    Methods: GET, PUT, DELETE, OPTIONS
    """
    queryset = Collection.objects.annotate(products_count=Count("products"))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {"message": "Unable to delete collection linked to product"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response({"status": True}, status=status.HTTP_204_NO_CONTENT)
