from decimal import Decimal
import math
from rest_framework import serializers
from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count', 'featured_product']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", 'title', 'slug',  'description', 'unit_price',
                  'inventory', 'collection', 'last_update']

    # collection = CollectionSerializer()
    # price_with_tax = serializers.SerializerMethodField(
    #     method_name="calc_tax_price")

    # def calc_tax_price(self, product):
    #     return product.unit_price * Decimal(1.1)
