from django.contrib import admin
from .models import AnnouncementCategory, Announcement


@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display  = ("slug", "title_en", "icon_class")
    list_editable = ("icon_class",)
    fieldsets = (
        ("Category Info", {
            "fields": ("slug", "icon_class"),
        }),
        ("Language Versions — Name", {
            "description": "Each field is the category name shown when a user switches to that language.",
            "fields": ("title_en", "title_ar", "title_ur", "title_fa"),
        }),
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display   = ("title_en", "category", "is_pinned", "is_active", "publish_date")
    list_filter    = ("category", "is_pinned", "is_active")
    list_editable  = ("is_pinned", "is_active")
    search_fields  = ("title_en", "title_ar", "title_ur", "title_fa")
    date_hierarchy = "publish_date"
    fieldsets = (
        ("English — Displayed when language is set to English", {
            "fields": ("category", "title_en", "body_en"),
        }),
        ("Arabic (العربية) — Displayed when language is set to Arabic", {
            "classes": ("collapse",),
            "fields": ("title_ar", "body_ar"),
        }),
        ("Urdu (اردو) — Displayed when language is set to Urdu", {
            "classes": ("collapse",),
            "fields": ("title_ur", "body_ur"),
        }),
        ("Persian / Farsi (فارسی) — Displayed when language is set to Persian", {
            "classes": ("collapse",),
            "fields": ("title_fa", "body_fa"),
        }),
        ("Media & Attachment", {
            "fields": ("image", "attachment"),
        }),
        ("Event Details — Fill only for items in the 'Event' category", {
            "classes": ("collapse",),
            "fields": ("event_date", "event_location", "youtube_url", "video_embed_code"),
        }),
        ("Visibility", {
            "fields": ("is_pinned", "is_active"),
        }),
    )
