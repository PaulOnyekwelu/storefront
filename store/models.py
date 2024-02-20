from django.db import models
from django.utils.translation import gettext_lazy as _


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=200)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)


class Customer(models.Model):
    class Membership(models.TextChoices):
        BRONZE = ("B", _("Bronze"))
        SILVER = ("S", _("Silver"))
        GOLD = ("G", _("Gold"))

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=Membership.choices, default=Membership.BRONZE
    )


class Address(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20, null=True)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = ("P", "Pending")
        COMPLETE = ("C", "Complete")
        FAILED = ("F", "Failed")

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.PENDING
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
