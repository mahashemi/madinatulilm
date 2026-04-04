import json
from django.shortcuts import render
from .models import (
    WelcomeSection, MissionSection, VisionSection, AboutSection,
    Founder, Ijazah, Trustee, AcademicProgram, MadrasahGallery,
    HadithQuote, PartnerPage, Maraji, HeroBannerImage
)
from announcements.models import Announcement
from lessons.models import Subject, LessonSeries
from books.models import Book


def _section_json(obj, *text_fields):
    """Serialize a multilingual section object to a dict with en/ar/ur/fa fields."""
    if obj is None:
        return {}
    data = {}
    for field in text_fields:
        for lang in ('en', 'ar', 'ur', 'fa'):
            key = f"{field}_{lang}"
            data[key] = getattr(obj, key, '') or ''
    return data


def home(request):
    welcome = WelcomeSection.objects.filter(is_active=True).first()
    mission = MissionSection.objects.filter(is_active=True).first()
    vision  = VisionSection.objects.filter(is_active=True).first()

    hadiths = list(HadithQuote.objects.filter(is_active=True).values(
        "text_ar", "text_en", "text_ur", "text_fa", "source", "narrator"
    ))

    page_content = {
        "welcome": _section_json(welcome, "title", "body"),
        "mission": _section_json(mission, "title", "body"),
        "vision":  _section_json(vision,  "title", "body"),
    }

    # Hero banner background images — serialised for JS crossfade.
    # Falls back to static/img/banner.jpeg when queryset is empty.
    hero_images = list(
        HeroBannerImage.objects.filter(is_active=True).values_list("image", flat=True)
    )

    context = {
        "hero_images_json": json.dumps(
            [f"/media/{url}" for url in hero_images],
            ensure_ascii=False
        ),
        "welcome":              welcome,
        "mission":              mission,
        "vision":               vision,
        "maraji":               Maraji.objects.filter(is_active=True).first(),
        "founder":              Founder.objects.filter(is_active=True).first(),
        "programs":             AcademicProgram.objects.filter(is_active=True)[:8],
        "latest_announcements": Announcement.objects.filter(is_active=True)[:4],
        "latest_lessons":       LessonSeries.objects.filter(is_active=True)[:4],
        "latest_books":         Book.objects.filter(is_active=True)[:4],
        "gallery":              MadrasahGallery.objects.filter(is_active=True)[:6],
        "hadiths_json":         json.dumps(hadiths,      ensure_ascii=False),
        "page_content_json":    json.dumps(page_content, ensure_ascii=False),
    }
    return render(request, "core/home.html", context)


def about(request):
    context = {
        "about": AboutSection.objects.filter(is_active=True).first(),
        "mission": MissionSection.objects.filter(is_active=True).first(),
        "vision": VisionSection.objects.filter(is_active=True).first(),
        "trustees": Trustee.objects.filter(is_active=True),
        "ijazat": Ijazah.objects.all().order_by("sort_order"),
        "gallery": MadrasahGallery.objects.filter(is_active=True),
    }
    return render(request, "core/about.html", context)


def founder(request):
    context = {
        "founder": Founder.objects.filter(is_active=True).first(),
        "ijazat": Ijazah.objects.all(),
    }
    return render(request, "core/founder.html", context)


def academics(request):
    context = {
        "programs": AcademicProgram.objects.filter(is_active=True),
        "subjects": Subject.objects.filter(is_active=True),
    }
    return render(request, "core/academics.html", context)


def gallery(request):
    context = {
        "gallery": MadrasahGallery.objects.filter(is_active=True),
    }
    return render(request, "core/gallery.html", context)


DONATION_ITEMS = [
    "Sahme Imam",
    "Sahme Sadaat",
    "Radde Mazalim",
    "Zakaat",
    "Sadqa",
    "Remberance for your Marhoomeen",
    "General Charity",
]


def partner(request):
    context = {
        "page": PartnerPage.objects.filter(is_active=True).first(),
        "donation_items": DONATION_ITEMS,
    }
    return render(request, "core/partner.html", context)
