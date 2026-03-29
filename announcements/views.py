from django.shortcuts import render, get_object_or_404
from .models import AnnouncementCategory, Announcement


def announcements_home(request):
    categories = AnnouncementCategory.objects.all()
    announcements = Announcement.objects.filter(is_active=True)
    context = {"categories": categories, "announcements": announcements}
    return render(request, "announcements/announcements_home.html", context)


def announcements_by_category(request, slug):
    category = get_object_or_404(AnnouncementCategory, slug=slug)
    announcements = category.announcements.filter(is_active=True)
    return render(request, "announcements/announcements_category.html", {"category": category, "announcements": announcements})


def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, is_active=True)
    return render(request, "announcements/announcement_detail.html", {"announcement": announcement})
