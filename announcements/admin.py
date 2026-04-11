from django.contrib import admin
from .models import AnnouncementCategory, Announcement, AnnouncementImage, Testimonial


# ─── Inline: images belong to an Announcement ────────────────────────────────
class AnnouncementImageInline(admin.TabularInline):
    model      = AnnouncementImage
    extra      = 3          # show 3 empty slots by default
    fields     = ("image", "caption", "sort_order")
    ordering   = ("sort_order", "id")


# ─── Category ────────────────────────────────────────────────────────────────
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


# ─── Announcement ─────────────────────────────────────────────────────────────
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display   = ("title_en", "category", "is_pinned", "is_active", "publish_date")
    list_filter    = ("category", "is_pinned", "is_active")
    list_editable  = ("is_pinned", "is_active")
    search_fields  = ("title_en", "title_ar", "title_ur", "title_fa")
    date_hierarchy = "publish_date"
    inlines        = [AnnouncementImageInline]

    fieldsets = (
        # ── Core content (all category types) ──────────────────────────────
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
        # ── Attachment (all category types) ────────────────────────────────
        ("Attachment", {
            "fields": ("attachment",),
        }),
        # ── Event-specific — only visible / relevant for slug == "event" ───
        ("Event Details  \u27f5  Fill only for announcements in the 'Event' category", {
            "classes": ("collapse",),
            "description": (
                "These fields only apply when the Category above is set to 'Event'. "
                "Upload multiple images using the Images section below — they will be "
                "shown in a carousel on the event detail page. "
                "You can also embed a YouTube link or raw iframe inside the body text above."
            ),
            "fields": ("event_date", "event_location", "youtube_url", "video_embed_code"),
        }),
        # ── Visibility ──────────────────────────────────────────────────────
        ("Visibility", {
            "fields": ("is_pinned", "is_active"),
        }),
    )


# ─── Testimonial ──────────────────────────────────────────────────────────────
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display   = ("author_name_en", "author_title_en", "is_featured", "is_active", "sort_order", "created_at")
    list_filter    = ("is_featured", "is_active")
    list_editable  = ("is_featured", "is_active", "sort_order")
    search_fields  = ("author_name_en", "author_name_ar", "author_name_ur", "quote_en")
    ordering       = ("sort_order", "-created_at")
    fieldsets = (
        ("Author — English", {
            "fields": ("author_name_en", "author_title_en", "author_photo"),
        }),
        ("Author — Arabic (العربية)", {
            "classes": ("collapse",),
            "fields": ("author_name_ar", "author_title_ar"),
        }),
        ("Author — Urdu (اردو)", {
            "classes": ("collapse",),
            "fields": ("author_name_ur", "author_title_ur"),
        }),
        ("Author — Persian (فارسی)", {
            "classes": ("collapse",),
            "fields": ("author_name_fa", "author_title_fa"),
        }),
        ("Quote (short — shown on home page cards)", {
            "description": "Keep this to 1–3 sentences. It appears on the home page testimonial strip.",
            "fields": ("quote_en", "quote_ar", "quote_ur", "quote_fa"),
        }),
        ("Full Description (shown on Testimonials page only)", {
            "classes": ("collapse",),
            "description": "Longer story or background — optional.",
            "fields": ("description_en", "description_ar", "description_ur", "description_fa"),
        }),
        ("Visibility & Ordering", {
            "fields": ("is_featured", "is_active", "sort_order"),
        }),
    )
