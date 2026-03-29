from django.contrib import admin
from .models import QuranResource


@admin.register(QuranResource)
class QuranResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "resource_type", "surah_number", "surah_name", "is_active", "created_at")
    list_filter = ("resource_type", "is_active")
    list_editable = ("is_active",)
    search_fields = ("title", "title_ar", "surah_name", "tags")
