from django.contrib import admin
from .models import BookCategory, Book


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("title_en", "slug", "sort_order")
    list_editable = ("sort_order",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title_en", "author", "category", "content_type", "language", "is_downloadable", "is_active", "download_count")
    list_filter = ("category", "content_type", "language", "is_active")
    list_editable = ("is_downloadable", "is_active")
    search_fields = ("title_en", "title_ar", "author")
    readonly_fields = ("download_count",)
