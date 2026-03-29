from django.contrib import admin
from .models import AnnouncementCategory, Announcement


@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ("title_en", "slug", "icon_class")


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title_en", "category", "publish_date", "is_pinned", "is_active")
    list_filter = ("category", "is_pinned", "is_active")
    list_editable = ("is_pinned", "is_active")
    search_fields = ("title_en", "title_ar", "title_ur")
    date_hierarchy = "publish_date"
