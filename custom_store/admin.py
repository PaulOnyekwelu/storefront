from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


# Register your models here.
class TaggedItemTabular(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ("tag",)


class CustomProductAdmin(ProductAdmin):
    inlines = (TaggedItemTabular,)


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
