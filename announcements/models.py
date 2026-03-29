"""
Announcements app models — Statements, Issued Messages, Meetings
"""
from django.db import models
from ckeditor.fields import RichTextField


class AnnouncementCategory(models.Model):
    SLUG_CHOICES = [
        ("statement", "Statement"),
        ("message", "Issued Message"),
        ("meeting", "Meeting"),
    ]
    slug = models.CharField(max_length=20, choices=SLUG_CHOICES, unique=True)
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, blank=True)
    icon_class = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Announcement Categories"

    def __str__(self):
        return self.title_en


class Announcement(models.Model):
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.CASCADE, related_name="announcements")
    title_en = models.CharField(max_length=400)
    title_ar = models.CharField(max_length=400, blank=True)
    title_ur = models.CharField(max_length=400, blank=True)
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    attachment = models.FileField(upload_to="announcements/", null=True, blank=True)
    image = models.ImageField(upload_to="announcements/images/", null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    publish_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-publish_date"]

    def __str__(self):
        return self.title_en
