from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models.aggregates import Count
from .models import Tag, TaggedItem


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ("tag", "content_type", "object_id", "content_object")
    list_filter = ("tag",)
    ordering = ("tag",)


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "tagged_items_count")
    ordering = ("title",)
    search_fields = ("title",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(tagged_items_count=Count("taggeditem"))
        )

    @admin.display(ordering="tagged_items_count")
    def tagged_items_count(self, tag):
        url = (
            reverse("admin:tags_taggeditem_changelist")
            + "?"
            + urlencode({"tag__id": tag.id})
        )
        return format_html(
            "<a href='{}'>{}</a>", url, f"{tag.tagged_items_count} item(s)"
        )
