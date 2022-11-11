from decimal import Decimal
import math
from rest_framework import serializers
from store import models


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ['id', 'title', 'products_count', 'featured_product']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ["id", 'title', 'slug',  'description', 'unit_price',
                  'inventory', 'collection', 'last_update']

    # collection = CollectionSerializer()
    # price_with_tax = serializers.SerializerMethodField(
    #     method_name="calc_tax_price")

    # def calc_tax_price(self, product):
    #     return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'date', 'description', 'username']

    username = serializers.SerializerMethodField()

    def get_username(self, review):
        return f"{review.customer.first_name} {review.customer.last_name}"

    def create(self, validated_data):
        product_id = self.context["product_id"]
        customer_id = models.Customer.objects.get(pk=1).id
        return models.Review.objects.create(
            product_id=product_id,
            customer_id=customer_id,
            **validated_data
        )
