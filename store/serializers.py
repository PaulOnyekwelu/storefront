from rest_framework import serializers
from store.models import Product


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    slug = serializers.SlugField()
    title = serializers.CharField(max_length=255)
    slug_custom = serializers.SerializerMethodField(
        method_name='get_slug_custom')
    description = serializers.CharField(max_length=2000)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source="unit_price")
    inventory = serializers.IntegerField()
    last_update = serializers.DateTimeField()
    collection = CollectionSerializer()

    def get_slug_custom(self, product: Product):
        return product.title.replace(" ", "_").lower()
