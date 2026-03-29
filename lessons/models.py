"""
Lessons app models — structured academic lessons by subject
"""
from django.db import models
from ckeditor.fields import RichTextField


class Subject(models.Model):
    SUBJECT_SLUG_CHOICES = [
        ("tafsir", "Tafsīr (Quranic Exegesis)"),
        ("hadith", "Hadith (Prophetic Traditions)"),
        ("fiqh", "Fiqh (Jurisprudence)"),
        ("usul", "Usūl al-Fiqh (Principles of Jurisprudence)"),
        ("kalam", "Kalām & ʿAqīdah (Theology & Creed)"),
        ("akhlaq", "Akhlāq (Ethics)"),
        ("rational", "Rational Sciences (Logic & Philosophy)"),
        ("arabic", "Language & Literature (Arabic, English, Persian)"),
    ]
    slug = models.CharField(max_length=20, choices=SUBJECT_SLUG_CHOICES, unique=True)
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, blank=True)
    description_en = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title_en


class LessonSeries(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="series")
    title_en = models.CharField(max_length=300)
    title_ar = models.CharField(max_length=300, blank=True)
    description_en = RichTextField(blank=True)
    instructor = models.CharField(max_length=200, blank=True)
    thumbnail = models.ImageField(upload_to="lessons/thumbnails/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Lesson Series"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject.title_en} — {self.title_en}"


class Lesson(models.Model):
    MEDIA_TYPE = [
        ("text", "Text"),
        ("pdf", "PDF"),
        ("audio", "Audio"),
        ("video", "Video"),
        ("mixed", "Mixed"),
    ]
    series = models.ForeignKey(LessonSeries, on_delete=models.CASCADE, related_name="lessons")
    title_en = models.CharField(max_length=300)
    title_ar = models.CharField(max_length=300, blank=True)
    lesson_number = models.PositiveIntegerField(default=1)
    content_en = RichTextField(blank=True)
    content_ar = RichTextField(blank=True)
    content_ur = RichTextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE, default="text")
    pdf_file = models.FileField(upload_to="lessons/pdfs/", null=True, blank=True)
    audio_file = models.FileField(upload_to="lessons/audio/", null=True, blank=True)
    video_file = models.FileField(upload_to="lessons/video/", null=True, blank=True)
    video_url = models.URLField(blank=True, help_text="YouTube/Vimeo embed URL")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["lesson_number"]
        unique_together = [["series", "lesson_number"]]

    def __str__(self):
        return f"{self.series.title_en} — Lesson {self.lesson_number}: {self.title_en}"
