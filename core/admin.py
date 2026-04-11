from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from .models import (
    SiteSettings, WelcomeSection, MissionSection, VisionSection,
    AboutSection, Founder, Ijazah, Trustee, AcademicProgram,
    MadrasahGallery, HadithQuote, PartnerPage, Maraji, HeroBannerImage
)

# ── Custom Admin Site Branding ─────────────────────────────────────────────
admin.site.site_header  = "Muhammadiyyah Trust — Admin"
admin.site.site_title   = "Muhammadiyyah Admin"
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
        ("Imam al-ʿAsr Bar (below Bismillah — site-wide)", {
            "fields": (
                "show_imamasr_bar",
                "imamasr_bar_en", "imamasr_bar_ar",
                "imamasr_bar_ur", "imamasr_bar_fa",
            ),
        }),
        ("Marājiʿ Panel Label (Homepage Hero)", {
            "description": "Label shown above the Marja's name in the homepage hero (e.g. 'In Memoriam…').",
            "fields": (
                "maraji_label_en", "maraji_label_ar",
                "maraji_label_ur", "maraji_label_fa",
            ),
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
    list_display  = ("name", "member_type", "designation", "phone", "is_founder", "is_active", "sort_order")
    list_filter   = ("member_type", "is_founder", "is_active")
    list_editable = ("member_type", "sort_order", "is_active")
    fieldsets = (
        ("Identity", {
            "fields": ("name", "designation", "member_type", "photo"),
        }),
        ("Contact", {
            "fields": ("phone", "bio"),
        }),
        ("Display", {
            "fields": ("is_founder", "is_active", "sort_order"),
        }),
    )


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


@admin.register(Maraji)
class MarajiAdmin(admin.ModelAdmin):
    """
    Admin for Marājiʿ (Shia Spiritual Authorities) displayed on the homepage banner.
    The banner automatically shows رحمة الله عليه when is_deceased is checked,
    or دام ظله الوارف when unchecked.
    """
    list_display  = ("name_en", "name_ar", "photo_preview", "is_deceased", "is_active", "sort_order", "updated_at")
    list_editable = ("is_active", "is_deceased", "sort_order")
    list_filter   = ("is_active", "is_deceased")
    readonly_fields = ("photo_preview", "honorific_preview")

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" height="80" style="border-radius:50%;object-fit:cover;'
                'border:3px solid #c9a84c;" />',
                obj.photo.url
            )
        return "— No photo uploaded —"
    photo_preview.short_description = "Portrait Preview"

    def honorific_preview(self, obj):
        """Live preview of the honorific that will appear on the banner."""
        color = "#c0392b" if obj.is_deceased else "#2d8a4e"
        ar    = obj.honorific_ar
        en    = obj.honorific_en
        return format_html(
            '<span style="font-family:Amiri,serif;font-size:1.2rem;color:{};direction:rtl;">{}</span>'
            '&nbsp;&nbsp;<span style="color:{};">— {}</span>',
            color, ar, color, en
        )
    honorific_preview.short_description = "Honorific shown on banner"

    fieldsets = (
        # ── Photo ──────────────────────────────────────────────────────────
        ("Portrait Photo", {
            "description": (
                "Upload the scholar's portrait photograph. It will appear in the homepage "
                "hero banner on the right side. Recommended: high-quality PNG/JPG, min 400×500px."
            ),
            "fields": ("photo", "photo_preview"),
        }),
        # ── Deceased / Status ──────────────────────────────────────────────
        ("Status & Honorific", {
            "description": (
                "⚠️  If the scholar has passed away, check 'Deceased'. The banner will "
                "automatically display  رحمة الله عليه  (Rahmatullāhi ʿAlayh) instead of "
                "دام ظله الوارف  (Dāma Ẓilluhū)."
            ),
            "fields": ("is_deceased", "date_of_passing", "honorific_preview", "is_active", "sort_order"),
        }),
        # ── English ────────────────────────────────────────────────────────
        ("English — shown when site language = English", {
            "fields": ("name_en", "title_en", "role_en", "description_en", "affiliation_en"),
        }),
        # ── Arabic ─────────────────────────────────────────────────────────
        ("Arabic (العربية) — shown when site language = Arabic", {
            "classes": ("collapse",),
            "description": "Fill all Arabic fields using Arabic script (right-to-left).",
            "fields": ("name_ar", "title_ar", "role_ar", "description_ar", "affiliation_ar"),
        }),
        # ── Urdu ───────────────────────────────────────────────────────────
        ("Urdu (اردو) — shown when site language = Urdu", {
            "classes": ("collapse",),
            "description": "Fill all Urdu fields using Urdu/Nastaliq script (right-to-left).",
            "fields": ("name_ur", "title_ur", "role_ur", "description_ur", "affiliation_ur"),
        }),
        # ── Persian ────────────────────────────────────────────────────────
        ("Persian / Farsi (فارسی) — shown when site language = Persian", {
            "classes": ("collapse",),
            "description": "Fill all Farsi fields using Persian script (right-to-left).",
            "fields": ("name_fa", "title_fa", "role_fa", "description_fa", "affiliation_fa"),
        }),
    )


@admin.register(HeroBannerImage)
class HeroBannerImageAdmin(admin.ModelAdmin):
    """
    Manage the rotating background images shown in the homepage hero banner.
    Images are displayed as a crossfade slideshow — add/remove/reorder here.
    """
    list_display  = ("__str__", "image_preview", "is_active", "sort_order", "uploaded_at")
    list_editable = ("is_active", "sort_order")
    ordering      = ("sort_order", "uploaded_at")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" height="60" style="object-fit:cover;border-radius:4px;'
                'border:1px solid #c9a84c;max-width:120px;" />',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Preview"

    fieldsets = (
        ("Image", {
            "description": (
                "Upload a landscape-orientation photo of the Madrasah building / grounds. "
                "Recommended size: 1600×900 px or larger. JPEG/WebP gives best compression."
            ),
            "fields": ("image", "caption"),
        }),
        ("Display", {
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
        ("🏦 Bank 1 Details", {
            "description": "These fields are displayed in the Bank Details section on the Be A Partner page.",
            "fields": (
                "bank1_name", "bank1_beneficiary", "bank1_branch",
                "bank1_account_no", "bank1_ifsc",
            ),
        }),
        ("🏦 Bank 2 Details", {
            "description": "Second bank account details (e.g. SBI).",
            "fields": (
                "bank2_name", "bank2_beneficiary", "bank2_branch",
                "bank2_account_no", "bank2_ifsc",
            ),
        }),
        ("📷 QR Codes", {
            "description": "Upload QR code images for each bank. Shown in the 'Scan to Pay' section.",
            "fields": ("qr_code_1", "qr_code_2"),
        }),
        ("📋 Other", {
            "fields": ("cheque_name", "tax_note", "is_active"),
        }),
    )
