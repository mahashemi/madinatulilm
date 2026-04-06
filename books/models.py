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


class UsefulLink(models.Model):
    """Curated external Islamic resource links shown on the Useful Links page."""
    CATEGORY_CHOICES = [
        ("maraji",    "Marājiʿ Offices"),
        ("quran",     "Qurʾān & Tafsīr"),
        ("hadith",    "Hadith & Rijāl"),
        ("dua",       "Duʿāʾ & Ziyārat"),
        ("sharia",    "Fiqh & Fatāwā"),
        ("education", "Islamic Education"),
        ("library",   "Digital Libraries"),
        ("other",     "Other Resources"),
    ]
    title       = models.CharField(max_length=200)
    url         = models.URLField()
    description = models.CharField(max_length=400, blank=True)
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    icon_class  = models.CharField(max_length=100, blank=True,
                                   help_text="Font Awesome icon class e.g. fas fa-globe")
    sort_order  = models.PositiveSmallIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "sort_order", "title"]
        verbose_name = "Useful Link"
        verbose_name_plural = "Useful Links"

    def __str__(self):
        return f"{self.title} ({self.url})"
