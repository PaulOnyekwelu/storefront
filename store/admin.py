from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Collection, Customer, Product, Order, OrderItem


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ("clear_inventory",)
    autocomplete_fields = ("collection",)
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
    list_filter = ("collection", InventoryFilter)
    list_per_page = 20
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ("title",)

    @admin.display(ordering="collection")
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        return "Low" if product.inventory < 50 else "Ok"

    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} product(s) successfully updated.",
            messages.ERROR,
        )


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "featured_product", "products_count")
    search_fields = ("title",)
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

        return format_html(
            "<a href='{}'>{}</a>", url, f"{collection.products_count} product(s)"
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "membership", "orders_count")
    list_display_links = ("full_name",)
    list_editable = ("membership",)
    ordering = ("first_name", "last_name")
    list_filter = ("order",)
    search_fields = ("first_name__istartswith", "last_name__istartswith")
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
        return format_html(
            "<a href='{}'>{}</a>", url, f"{customer.orders_count} order(s)"
        )


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ("product",)
    min_num = 1
    max_num = 10
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ("customer",)
    inlines = [OrderItemInLine]
    list_display = (
        "order_id",
        "order_items",
        "placed_at",
        "customer_name",
        "payment_status",
    )
    list_filter = ("customer", "payment_status")
    list_select_related = ("customer",)
    list_per_page = 20
    ordering = ("customer",)

    def get_queryset(self, request):
        return (
            super().get_queryset(request).annotate(orderitems_count=Count("orderitem"))
        )

    @admin.display(ordering="id")
    def order_id(self, order):
        return order.id

    @admin.display(ordering="order_items")
    def order_items(self, order):
        url = (
            reverse("admin:store_orderitem_changelist")
            + "?"
            + urlencode({"order__id": order.id})
        )
        return format_html(
            "<a href='{}'>{}</a>", url, f"{order.orderitems_count} items"
        )

    @admin.display(ordering="customer")
    def customer_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "unit_price", "order_id")
    list_filter = ("order",)

    @admin.display(ordering="order_id")
    def order_id(self, order_item):
        return order_item.order.id
