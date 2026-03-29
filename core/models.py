"""
Core models — site-wide content: homepage, about, founder, trustees, academics
"""
from django.db import models
from ckeditor.fields import RichTextField


class SiteSettings(models.Model):
    """Global site configuration — only one row expected."""
    site_name_en = models.CharField(max_length=200, default="Madrasah Madinatul Ilm")
    site_name_ar = models.CharField(max_length=200, default="مدرسة مدينة العلم")
    site_name_ur = models.CharField(max_length=200, default="مدرسہ مدینۃ العلم")
    tagline_en = models.CharField(max_length=300, default="Centre of Fiqāhat")
    trust_name = models.CharField(max_length=200, default="Muhammadiyah Trust")
    established = models.DateField(null=True, blank=True)
    logo = models.ImageField(upload_to="site/", null=True, blank=True)
    favicon = models.ImageField(upload_to="site/", null=True, blank=True)
    hero_image = models.ImageField(upload_to="site/", null=True, blank=True)
    address = models.TextField(blank=True)
    phone_primary = models.CharField(max_length=30, blank=True)
    phone_secondary = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    google_maps_embed = models.TextField(blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name_en


class WelcomeSection(models.Model):
    title_en = models.CharField(max_length=300)
    title_ar = models.CharField(max_length=300, blank=True)
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class MissionSection(models.Model):
    title_en = models.CharField(max_length=300, default="Our Mission")
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class VisionSection(models.Model):
    title_en = models.CharField(max_length=300, default="Our Vision")
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class AboutSection(models.Model):
    title_en = models.CharField(max_length=300, default="About Us")
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class Founder(models.Model):
    name_en = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)
    name_ur = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=300, blank=True)
    photo = models.ImageField(upload_to="founder/", null=True, blank=True)
    biography_en = RichTextField(blank=True)
    biography_ur = RichTextField(blank=True)
    biography_ar = RichTextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.name_en


class Ijazah(models.Model):
    IJAZAH_TYPE_CHOICES = [
        ("riwayat", "Ijazah Naql Riwayat"),
        ("wakalat", "Ijazah Wakalat"),
        ("sahm_imam", "Ijazah Sahm Imam"),
        ("other", "Other"),
    ]
    title = models.CharField(max_length=300)
    from_scholar = models.CharField(max_length=200)
    ijazah_type = models.CharField(max_length=20, choices=IJAZAH_TYPE_CHOICES, default="riwayat")
    image = models.ImageField(upload_to="ijazat/")
    description = models.TextField(blank=True)
    date_received = models.DateField(null=True, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "from_scholar"]
        verbose_name_plural = "Ijazat"

    def __str__(self):
        return f"{self.ijazah_type} — {self.from_scholar}"


class Trustee(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to="trustees/", null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class AcademicProgram(models.Model):
    SUBJECT_CHOICES = [
        ("quran", "Qurʾān"),
        ("hadith", "Hadith"),
        ("fiqh", "Fiqh"),
        ("usul", "Usūl al-Fiqh"),
        ("kalam", "Kalām & ʿAqīdah"),
        ("akhlaq", "Akhlāq"),
        ("rational", "Rational Sciences"),
        ("language", "Language & Literature"),
    ]
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, blank=True)
    description_en = RichTextField(blank=True)
    description_ar = RichTextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class")
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title_en


class MadrasahGallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Madrasah Gallery"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title
