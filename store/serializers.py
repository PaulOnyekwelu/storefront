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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ["id", "title", "unit_price"]


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


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ["id", "product", "quantity", "total_price"]

    # product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, item):
        return item.quantity * item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ["id", "items", "total_price"]

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([
            item.quantity * item.product.unit_price
            for item in cart.items.all()
        ])
