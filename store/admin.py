from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Collection, Customer, Product, Order


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "featured_product", "products_count")
    ordering = ("title",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))

    @admin.display(ordering="products_count")
    def products_count(self, collection):

        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": collection.id})
        )

        return format_html("<a href='{}'>{}</a>", url, collection.products_count)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "unit_price",
        "inventory",
        "inventory_status",
        "collection_title",
    )
    list_editable = ("unit_price", "inventory")
    list_display_links = ("title", "description")
    list_select_related = ("collection",)
    list_filter = ("collection",)
    list_per_page = 20

    @admin.display(ordering="collection")
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        return "Low" if product.inventory < 50 else "Ok"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "membership", "orders_count")
    list_display_links = ("full_name",)
    list_editable = ("membership",)
    ordering = ("first_name", "last_name")
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))

    @admin.display(ordering="full_name")
    def full_name(self, customer):
        return f"{customer.first_name} {customer.last_name}"

    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": customer.id})
        )
        return format_html("<a href='{}'>{}</a>", url, customer.orders_count)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "placed_at", "customer_name", "payment_status")
    ordering = ("customer",)
    list_filter = ("customer", "payment_status")
    list_per_page = 20

    @admin.display(ordering="id")
    def order_id(self, order):
        return order.id

    @admin.display(ordering="customer")
    def customer_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"
