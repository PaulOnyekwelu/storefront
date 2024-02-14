from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class LikedItem(models.Model):
    RELATED_NAME = "liked_items"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=RELATED_NAME)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name=RELATED_NAME
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
