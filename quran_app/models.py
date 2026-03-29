"""
Quran app models
"""
from django.db import models
from ckeditor.fields import RichTextField


class QuranResource(models.Model):
    RESOURCE_TYPE = [
        ("text", "Text / Article"),
        ("pdf", "PDF"),
        ("audio", "Audio Recitation"),
        ("video", "Video"),
    ]
    title = models.CharField(max_length=300)
    title_ar = models.CharField(max_length=300, blank=True)
    description = RichTextField(blank=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE, default="text")
    file = models.FileField(upload_to="quran/files/", null=True, blank=True)
    external_url = models.URLField(blank=True)
    surah_number = models.PositiveSmallIntegerField(null=True, blank=True)
    surah_name = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Quran Resource"

    def __str__(self):
        return self.title
