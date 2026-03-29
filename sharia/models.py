"""
Sharia app models — Kalam/Aqeedah, Akhlaq, Fiqh topics
"""
from django.db import models
from ckeditor.fields import RichTextField


class ShariaCategory(models.Model):
    CATEGORY_CHOICES = [
        ("kalam", "Kalām & ʿAqīdah (Theology & Creed)"),
        ("akhlaq", "Akhlāq (Ethics)"),
        ("fiqh", "Fiqh (Jurisprudence)"),
    ]
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Sharia Categories"

    def __str__(self):
        return self.title_en


class ShariaContent(models.Model):
    category = models.ForeignKey(ShariaCategory, on_delete=models.CASCADE, related_name="contents")
    title_en = models.CharField(max_length=300)
    title_ar = models.CharField(max_length=300, blank=True)
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    pdf_file = models.FileField(upload_to="sharia/pdfs/", null=True, blank=True)
    tags = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sharia Content"

    def __str__(self):
        return self.title_en
