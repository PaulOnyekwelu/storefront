import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    title = models.CharField(max_length=255)
    decription = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    class Membership(models.TextChoices):
        BRONZE = ("B", _("Bronze"))
        SILVER = ("S", _("Silver"))
        GOLD = ("G", _("Gold"))

    id = models.BigAutoField(primary_key=True, unique=True)
    pk = models.UUIDField(default=uuid.uuid4, unique=True, null=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=Membership.Choices, default=Membership.BRONZE
    )


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = ("P", "Pending")
        COMPLETE = ("C", "Complete")
        FAILED = ("F", "Failed")

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.Pending
    )
