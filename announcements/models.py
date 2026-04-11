"""
Announcements app models — Statements, Issued Messages, Events, Testimonials
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

    @property
    def first_image(self):
        """Return the first AnnouncementImage for this announcement, or None."""
        return self.images.order_by("sort_order", "id").first()


class AnnouncementImage(models.Model):
    """
    One image slide belonging to an Announcement.
    Multiple images per announcement → carousel on the detail page.
    """
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image      = models.ImageField(upload_to="announcements/images/")
    caption    = models.CharField(max_length=300, blank=True, help_text="Short caption shown below this image")
    sort_order = models.PositiveSmallIntegerField(default=0, help_text="Lower number = shown first")

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"Image {self.sort_order} — {self.announcement.title_en[:40]}"


# ─────────────────────────────────────────────────────────────
#  Testimonial
# ─────────────────────────────────────────────────────────────
class Testimonial(models.Model):
    """
    Community testimonial — students, parents, alumni, visiting scholars.

    • quote_*        → short pull-quote shown on home page cards (1–3 sentences)
    • description_*  → longer text shown only on the full testimonials page
    • is_featured    → show on home page (max 4 displayed)
    • is_active      → visibility toggle
    """

    # ── Author info (4 languages) ──
    author_name_en = models.CharField(max_length=200, verbose_name="Author name (EN)")
    author_name_ar = models.CharField(max_length=200, blank=True, verbose_name="Author name (AR)")
    author_name_ur = models.CharField(max_length=200, blank=True, verbose_name="Author name (UR)")
    author_name_fa = models.CharField(max_length=200, blank=True, verbose_name="Author name (FA)")

    author_title_en = models.CharField(max_length=200, blank=True, verbose_name="Author title / role (EN)",
                                       help_text="e.g. Student, Parent, Alumnus, Visiting Scholar")
    author_title_ar = models.CharField(max_length=200, blank=True, verbose_name="Author title (AR)")
    author_title_ur = models.CharField(max_length=200, blank=True, verbose_name="Author title (UR)")
    author_title_fa = models.CharField(max_length=200, blank=True, verbose_name="Author title (FA)")

    author_photo = models.ImageField(
        upload_to="testimonials/photos/", null=True, blank=True,
        help_text="Optional portrait photo"
    )

    # ── Short pull-quote shown on home page ──
    quote_en = models.TextField(verbose_name="Quote (EN)")
    quote_ar = models.TextField(blank=True, verbose_name="Quote (AR)")
    quote_ur = models.TextField(blank=True, verbose_name="Quote (UR)")
    quote_fa = models.TextField(blank=True, verbose_name="Quote (FA)")

    # ── Longer description shown on full testimonials page ──
    description_en = models.TextField(blank=True, verbose_name="Full description (EN)")
    description_ar = models.TextField(blank=True, verbose_name="Full description (AR)")
    description_ur = models.TextField(blank=True, verbose_name="Full description (UR)")
    description_fa = models.TextField(blank=True, verbose_name="Full description (FA)")

    # ── Flags ──
    is_featured = models.BooleanField(
        default=False,
        help_text="Show this testimonial on the home page (up to 4 featured displayed)"
    )
    is_active   = models.BooleanField(default=True, help_text="Uncheck to hide from all pages")
    sort_order  = models.PositiveIntegerField(default=0, help_text="Lower = displayed first")
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.author_name_en} — {self.author_title_en or 'Testimonial'}"
