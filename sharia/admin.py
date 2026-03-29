from django.contrib import admin
from .models import ShariaCategory, ShariaContent


@admin.register(ShariaCategory)
class ShariaCategoryAdmin(admin.ModelAdmin):
    list_display = ("title_en", "name", "icon_class")


@admin.register(ShariaContent)
class ShariaContentAdmin(admin.ModelAdmin):
    list_display = ("title_en", "category", "is_active", "created_at")
    list_filter = ("category", "is_active")
    list_editable = ("is_active",)
    search_fields = ("title_en", "title_ar", "tags")
