from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from .models import (
    SiteSettings, WelcomeSection, MissionSection, VisionSection,
    AboutSection, Founder, Ijazah, Trustee, AcademicProgram,
    MadrasahGallery, HadithQuote, PartnerPage
)

# ── Custom Admin Site Branding ─────────────────────────────────────────────
admin.site.site_header  = "Muhammadiyah Trust — Admin"
admin.site.site_title   = "Muhammadiyah Admin"
admin.site.index_title  = "Madrasah Madinatul Ilm — Dashboard"


# ── Helpers ───────────────────────────────────────────────────────────────
LANG_NOTE = ("Each language version is shown to users when they switch the site language "
             "using the top-bar language selector (EN / AR / UR / FA).")


def lang_fieldset(fields, label_suffix="Content"):
    """Returns a standard 4-language fieldset tuple for admin forms."""
    return (
        ("English — shown when site language = English", {
            "fields": tuple(f + "_en" for f in fields) if isinstance(fields, list) else fields[0],
        }),
        ("Arabic (العربية) — shown when site language = Arabic", {
            "classes": ("collapse",),
            "fields": tuple(f + "_ar" for f in fields) if isinstance(fields, list) else fields[1],
        }),
        ("Urdu (اردو) — shown when site language = Urdu", {
            "classes": ("collapse",),
            "fields": tuple(f + "_ur" for f in fields) if isinstance(fields, list) else fields[2],
        }),
        ("Persian / Farsi (فارسی) — shown when site language = Persian", {
            "classes": ("collapse",),
            "fields": tuple(f + "_fa" for f in fields) if isinstance(fields, list) else fields[3],
        }),
    )


# ── Admins ────────────────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Site Identity", {
            "fields": ("site_name_en", "site_name_ar", "site_name_ur", "tagline_en",
                       "trust_name", "established", "logo", "favicon", "hero_image"),
        }),
        ("Contact Details", {
            "fields": ("address", "phone_primary", "phone_secondary", "email", "whatsapp_number"),
        }),
        ("Social Media", {
            "fields": ("facebook_url", "twitter_url", "youtube_url"),
        }),
        ("Maps", {
            "fields": ("google_maps_embed",),
        }),
    )


@admin.register(WelcomeSection)
class WelcomeSectionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "is_active", "updated_at")
    list_editable = ("is_active",)
    fieldsets = (
        ("English — shown when site language = English", {
            "fields": ("title_en", "body_en", "is_active"),
        }),
        ("Arabic (العربية) — shown when site language = Arabic", {
            "classes": ("collapse",),
            "fields": ("body_ar",),
        }),
        ("Urdu (اردو) — shown when site language = Urdu", {
            "classes": ("collapse",),
            "fields": ("body_ur",),
        }),
    )


@admin.register(MissionSection)
class MissionSectionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "is_active", "updated_at")
    fieldsets = (
        ("English — shown when site language = English", {
            "fields": ("title_en", "body_en", "is_active"),
        }),
        ("Arabic (العربية) — shown when site language = Arabic", {
            "classes": ("collapse",),
            "fields": ("body_ar",),
        }),
        ("Urdu (اردو) — shown when site language = Urdu", {
            "classes": ("collapse",),
            "fields": ("body_ur",),
        }),
    )


@admin.register(VisionSection)
class VisionSectionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "is_active", "updated_at")
    fieldsets = (
        ("English — shown when site language = English", {
            "fields": ("title_en", "body_en", "is_active"),
        }),
        ("Arabic (العربية) — shown when site language = Arabic", {
            "classes": ("collapse",),
            "fields": ("body_ar",),
        }),
        ("Urdu (اردو) — shown when site language = Urdu", {
            "classes": ("collapse",),
            "fields": ("body_ur",),
        }),
    )


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "is_active", "updated_at")
    fieldsets = (
        ("English — shown when site language = English", {
            "fields": ("title_en", "body_en", "is_active"),
        }),
        ("Arabic (العربية) — shown when site language = Arabic", {
            "classes": ("collapse",),
            "fields": ("body_ar",),
        }),
        ("Urdu (اردو) — shown when site language = Urdu", {
            "classes": ("collapse",),
            "fields": ("body_ur",),
        }),
    )


@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ("name_en", "title_en", "photo_preview", "phone", "is_active", "sort_order")
    list_editable = ("sort_order", "is_active")
    readonly_fields = ("photo_preview",)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" height="60" style="border-radius:50%;object-fit:cover;" />', obj.photo.url)
        return "No photo"
    photo_preview.short_description = "Photo"

    fieldsets = (
        ("Founder Photo", {
            "description": "Upload the founder's photo here. It will appear on the homepage founder section and the Founder page.",
            "fields": ("photo", "photo_preview"),
        }),
        ("English — shown when site language = English", {
            "fields": ("name_en", "title_en", "biography_en", "phone", "email", "is_active", "sort_order"),
        }),
        ("Arabic (العربية) — shown when site language = Arabic", {
            "classes": ("collapse",),
            "fields": ("name_ar", "biography_ar"),
        }),
        ("Urdu (اردو) — shown when site language = Urdu", {
            "classes": ("collapse",),
            "fields": ("name_ur", "biography_ur"),
        }),
    )


@admin.register(Ijazah)
class IjazahAdmin(admin.ModelAdmin):
    list_display = ("title", "from_scholar", "ijazah_type", "date_received", "sort_order")
    list_filter  = ("ijazah_type",)
    list_editable = ("sort_order",)


@admin.register(Trustee)
class TrusteeAdmin(admin.ModelAdmin):
    list_display  = ("name", "designation", "phone", "is_active", "sort_order")
    list_editable = ("sort_order", "is_active")


@admin.register(AcademicProgram)
class AcademicProgramAdmin(admin.ModelAdmin):
    list_display  = ("title_en", "subject", "is_active", "sort_order")
    list_filter   = ("subject", "is_active")
    list_editable = ("sort_order", "is_active")


@admin.register(MadrasahGallery)
class MadrasahGalleryAdmin(admin.ModelAdmin):
    list_display  = ("title", "is_active", "uploaded_at")
    list_editable = ("is_active",)


@admin.register(HadithQuote)
class HadithQuoteAdmin(admin.ModelAdmin):
    list_display  = ("narrator", "source_short", "is_active", "sort_order")
    list_editable = ("sort_order", "is_active")
    list_filter   = ("is_active",)
    search_fields = ("text_ar", "text_en", "narrator", "source")
    readonly_fields = ("source_short",)

    def source_short(self, obj):
        return obj.source[:60] + "…" if len(obj.source) > 60 else obj.source
    source_short.short_description = "Source"

    fieldsets = (
        ("Arabic (العربية) — Primary language of hadith", {
            "description": "Enter the hadith in Arabic. This is always shown.",
            "fields": ("text_ar", "narrator", "source"),
        }),
        ("English — shown when site language = English", {
            "classes": ("collapse",),
            "fields": ("text_en",),
        }),
        ("Urdu (اردو) — shown when site language = Urdu", {
            "classes": ("collapse",),
            "fields": ("text_ur",),
        }),
        ("Persian / Farsi (فارسی) — shown when site language = Persian", {
            "classes": ("collapse",),
            "fields": ("text_fa",),
        }),
        ("Display Settings", {
            "fields": ("is_active", "sort_order"),
        }),
    )


@admin.register(PartnerPage)
class PartnerPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("English — shown when site language = English", {
            "fields": ("intro_en",),
        }),
        ("Arabic (العربية) — shown when site language = Arabic", {
            "classes": ("collapse",),
            "fields": ("intro_ar",),
        }),
        ("Urdu (اردو) — shown when site language = Urdu", {
            "classes": ("collapse",),
            "fields": ("intro_ur",),
        }),
        ("Persian / Farsi (فارسی) — shown when site language = Persian", {
            "classes": ("collapse",),
            "fields": ("intro_fa",),
        }),
        ("Bank Details & QR Codes", {
            "fields": ("bank_details", "qr_code_1", "qr_code_2"),
        }),
        ("Other", {
            "fields": ("tax_note", "is_active"),
        }),
    )
