"""
Books & Articles app models
"""
from django.db import models
from ckeditor.fields import RichTextField


class BookCategory(models.Model):
    CATEGORY_CHOICES = [
        ("tafsir_hadith", "Tafsīr & Hadith"),
        ("rijal", "Rijāl (Science of Narrators)"),
        ("Fiqh", "Fiqh (Jurisprudence)"),
        ("usul", "Usūl al-Fiqh"),
        ("kalam", "Kalām & ʿAqīdah"),
        ("akhlaq", "Akhlāq (Ethics)"),
        ("rational", "Rational Sciences"),
        ("arabic", "Arabic Literature"),
        ("misc", "Miscellaneous"),
    ]
    slug = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, blank=True)
    icon_class = models.CharField(max_length=100, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name_plural = "Book Categories"

    def __str__(self):
        return self.title_en


class Book(models.Model):
    CONTENT_TYPE = [
        ("book", "Book"),
        ("article", "Article"),
        ("research", "Research Paper"),
        ("fatwa", "Fatwa Collection"),
    ]
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name="books")
    title_en = models.CharField(max_length=400)
    title_ar = models.CharField(max_length=400, blank=True)
    title_ur = models.CharField(max_length=400, blank=True)
    author = models.CharField(max_length=300, blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE, default="book")
    description_en = RichTextField(blank=True)
    description_ar = RichTextField(blank=True)
    cover_image = models.ImageField(upload_to="books/covers/", null=True, blank=True)
    pdf_file = models.FileField(upload_to="books/pdfs/", null=True, blank=True)
    external_url = models.URLField(blank=True)
    language = models.CharField(max_length=100, blank=True, default="Arabic")
    pages = models.PositiveIntegerField(null=True, blank=True)
    published_year = models.CharField(max_length=10, blank=True)
    is_downloadable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title_en
