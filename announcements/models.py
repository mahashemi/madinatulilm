"""
Announcements app models — Statements, Issued Messages, Events
"""
from django.db import models
from ckeditor.fields import RichTextField


class AnnouncementCategory(models.Model):
    SLUG_CHOICES = [
        ("statement", "Statement"),
        ("message",   "Issued Message"),
        ("event",     "Event"),
    ]
    slug     = models.CharField(max_length=20, choices=SLUG_CHOICES, unique=True)
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, blank=True)
    title_ur = models.CharField(max_length=200, blank=True)
    title_fa = models.CharField(max_length=200, blank=True)
    icon_class = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Announcement Categories"

    def __str__(self):
        return self.title_en


class Announcement(models.Model):
    category   = models.ForeignKey(AnnouncementCategory, on_delete=models.CASCADE, related_name="announcements")
    title_en   = models.CharField(max_length=400)
    title_ar   = models.CharField(max_length=400, blank=True)
    title_ur   = models.CharField(max_length=400, blank=True)
    title_fa   = models.CharField(max_length=400, blank=True)
    body_en    = RichTextField()
    body_ar    = RichTextField(blank=True)
    body_ur    = RichTextField(blank=True)
    body_fa    = RichTextField(blank=True)
    attachment = models.FileField(upload_to="announcements/", null=True, blank=True)
    image      = models.ImageField(upload_to="announcements/images/", null=True, blank=True)
    # Event-specific fields (used when category.slug == "event")
    event_date       = models.DateField(null=True, blank=True, help_text="Date of the event")
    event_location   = models.CharField(max_length=300, blank=True, help_text="Location / venue")
    youtube_url      = models.URLField(blank=True, help_text="YouTube live/recording link")
    video_embed_code = models.TextField(blank=True, help_text="Raw iframe embed code for any video platform")
    is_pinned  = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)
    publish_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-publish_date"]

    def __str__(self):
        return self.title_en

    @property
    def youtube_embed_url(self):
        """Convert a youtube watch URL to embed URL automatically."""
        if not self.youtube_url:
            return ""
        url = self.youtube_url
        if "watch?v=" in url:
            vid = url.split("watch?v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{vid}"
        if "youtu.be/" in url:
            vid = url.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{vid}"
        return url
