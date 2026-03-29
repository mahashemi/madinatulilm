from django.contrib import admin
from .models import (
    SiteSettings, WelcomeSection, MissionSection, VisionSection,
    AboutSection, Founder, Ijazah, Trustee, AcademicProgram, MadrasahGallery
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Site Identity", {"fields": ("site_name_en", "site_name_ar", "site_name_ur", "tagline_en", "trust_name", "established", "logo", "favicon", "hero_image")}),
        ("Contact", {"fields": ("address", "phone_primary", "phone_secondary", "email", "whatsapp_number")}),
        ("Social Media", {"fields": ("facebook_url", "twitter_url", "youtube_url")}),
        ("Maps", {"fields": ("google_maps_embed",)}),
    )


@admin.register(WelcomeSection)
class WelcomeSectionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "is_active", "updated_at")
    list_editable = ("is_active",)


@admin.register(MissionSection)
class MissionSectionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "is_active", "updated_at")


@admin.register(VisionSection)
class VisionSectionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "is_active", "updated_at")


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "is_active", "updated_at")


@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ("name_en", "title_en", "phone", "is_active", "sort_order")
    list_editable = ("sort_order", "is_active")


@admin.register(Ijazah)
class IjazahAdmin(admin.ModelAdmin):
    list_display = ("title", "from_scholar", "ijazah_type", "date_received", "sort_order")
    list_filter = ("ijazah_type",)
    list_editable = ("sort_order",)


@admin.register(Trustee)
class TrusteeAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "phone", "is_active", "sort_order")
    list_editable = ("sort_order", "is_active")


@admin.register(AcademicProgram)
class AcademicProgramAdmin(admin.ModelAdmin):
    list_display = ("title_en", "subject", "is_active", "sort_order")
    list_filter = ("subject", "is_active")
    list_editable = ("sort_order", "is_active")


@admin.register(MadrasahGallery)
class MadrasahGalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "uploaded_at")
    list_editable = ("is_active",)
