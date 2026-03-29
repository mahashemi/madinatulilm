from django.shortcuts import render
from .models import (
    WelcomeSection, MissionSection, VisionSection, AboutSection,
    Founder, Ijazah, Trustee, AcademicProgram, MadrasahGallery
)
from announcements.models import Announcement
from lessons.models import Subject, LessonSeries
from books.models import Book


def home(request):
    context = {
        "welcome": WelcomeSection.objects.filter(is_active=True).first(),
        "mission": MissionSection.objects.filter(is_active=True).first(),
        "vision": VisionSection.objects.filter(is_active=True).first(),
        "programs": AcademicProgram.objects.filter(is_active=True)[:8],
        "latest_announcements": Announcement.objects.filter(is_active=True)[:4],
        "latest_lessons": LessonSeries.objects.filter(is_active=True)[:4],
        "latest_books": Book.objects.filter(is_active=True)[:4],
        "gallery": MadrasahGallery.objects.filter(is_active=True)[:6],
    }
    return render(request, "core/home.html", context)


def about(request):
    context = {
        "about": AboutSection.objects.filter(is_active=True).first(),
        "mission": MissionSection.objects.filter(is_active=True).first(),
        "vision": VisionSection.objects.filter(is_active=True).first(),
        "trustees": Trustee.objects.filter(is_active=True),
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
