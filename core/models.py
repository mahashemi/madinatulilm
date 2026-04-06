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
    tagline_en = models.CharField(max_length=300, default="Centre of Faqāhat")
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
    title_ur = models.CharField(max_length=300, blank=True)
    title_fa = models.CharField(max_length=300, blank=True)
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    body_fa = RichTextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class MissionSection(models.Model):
    title_en = models.CharField(max_length=300, default="Our Mission")
    title_ar = models.CharField(max_length=300, blank=True, default="مهمتنا")
    title_ur = models.CharField(max_length=300, blank=True, default="ہمارا مشن")
    title_fa = models.CharField(max_length=300, blank=True, default="مأموریت ما")
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    body_fa = RichTextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class VisionSection(models.Model):
    title_en = models.CharField(max_length=300, default="Our Vision")
    title_ar = models.CharField(max_length=300, blank=True, default="رؤيتنا")
    title_ur = models.CharField(max_length=300, blank=True, default="ہمارا وژن")
    title_fa = models.CharField(max_length=300, blank=True, default="چشم‌انداز ما")
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    body_fa = RichTextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class AboutSection(models.Model):
    title_en = models.CharField(max_length=300, default="About Us")
    title_ar = models.CharField(max_length=300, blank=True, default="من نحن")
    title_ur = models.CharField(max_length=300, blank=True, default="ہمارے بارے میں")
    title_fa = models.CharField(max_length=300, blank=True, default="درباره ما")
    body_en = RichTextField()
    body_ar = RichTextField(blank=True)
    body_ur = RichTextField(blank=True)
    body_fa = RichTextField(blank=True)
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
    biography_fa = RichTextField(blank=True)
    phone = models.CharField(max_length=60, blank=True)
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
    image = models.ImageField(upload_to="ijazah/")
    description = models.TextField(blank=True)
    date_received = models.DateField(null=True, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "from_scholar"]
        verbose_name_plural = "Ijazah"

    def __str__(self):
        return f"{self.ijazah_type} — {self.from_scholar}"


class Trustee(models.Model):
    MEMBER_TYPE_CHOICES = [
        ("trustee",    "Trustee"),
        ("consultant", "Consulting Member"),
    ]

    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to="team/", null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_founder = models.BooleanField(
        default=False,
        verbose_name="Is Founder",
        help_text="Mark this trustee as the founder. Their card on the Trustees tab will link to the Founder biography page."
    )
    member_type = models.CharField(
        max_length=20,
        choices=MEMBER_TYPE_CHOICES,
        default="trustee",
        verbose_name="Member Type",
        help_text="Select 'Trustee' for board members or 'Consulting Member' for advisory/consulting members."
    )

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Our Team"

    def __str__(self):
        return f"{self.name} ({self.get_member_type_display()})"


class AcademicProgram(models.Model):
    SUBJECT_CHOICES = [
        ("quran", "Qurʾān"),
        ("hadith", "Hadith"),
        ("Fiqh", "Fiqh"),
        ("usul", "Usūl al-Fiqh"),
        ("kalam", "Kalām & ʿAqīdah"),
        ("akhlaq", "Akhlāq"),
        ("rational", "Rational Sciences"),
        ("language", "Language & Literature"),
    ]
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, blank=True)
    title_ur = models.CharField(max_length=200, blank=True)
    title_fa = models.CharField(max_length=200, blank=True)
    description_en = RichTextField(blank=True)
    description_ar = RichTextField(blank=True)
    description_ur = RichTextField(blank=True)
    description_fa = RichTextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class")
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title_en


class HadithQuote(models.Model):
    """Rotating hadith about ʿIlm displayed on the homepage."""
    text_ar   = models.TextField(help_text="Arabic text of the hadith")
    text_en   = models.TextField(blank=True, help_text="English translation")
    text_ur   = models.TextField(blank=True, help_text="Urdu translation")
    text_fa   = models.TextField(blank=True, help_text="Persian translation")
    source    = models.CharField(max_length=300, help_text="e.g. Al-Kafi, Vol.1, p.30")
    narrator  = models.CharField(max_length=200, blank=True, help_text="e.g. Imam Ali (AS)")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Hadith Quote"
        verbose_name_plural = "Hadith Quotes (ʿIlm)"

    def __str__(self):
        return f"{self.narrator or 'Hadith'} — {self.source}"


class PartnerPage(models.Model):
    """Be A Partner / donation page content — all fields editable from Admin."""
    intro_en   = models.TextField(blank=True)
    intro_ar   = models.TextField(blank=True)
    intro_ur   = models.TextField(blank=True)
    intro_fa   = models.TextField(blank=True)

    # ── Bank 1 (e.g. ICICI) ────────────────────────────────────────────────
    bank1_name        = models.CharField(max_length=200, blank=True, default="ICICI Bank",
                                         help_text="Display name, e.g. ICICI Bank")
    bank1_beneficiary = models.CharField(max_length=300, blank=True,
                                         default="Muhammadiyyah Educational & Social Welfare Trust")
    bank1_branch      = models.CharField(max_length=200, blank=True, default="Siwan, Bihar")
    bank1_account_no  = models.CharField(max_length=50, blank=True, help_text="Account number")
    bank1_ifsc        = models.CharField(max_length=20, blank=True, help_text="IFSC / Swift code")

    # ── Bank 2 (e.g. SBI) ──────────────────────────────────────────────────
    bank2_name        = models.CharField(max_length=200, blank=True, default="State Bank of India",
                                         help_text="Display name, e.g. State Bank of India")
    bank2_beneficiary = models.CharField(max_length=300, blank=True,
                                         default="Muhammadiyyah Educational & Social Welfare Trust")
    bank2_branch      = models.CharField(max_length=200, blank=True, default="Gopal Pur, Bihar")
    bank2_account_no  = models.CharField(max_length=50, blank=True, help_text="Account number")
    bank2_ifsc        = models.CharField(max_length=20, blank=True, help_text="IFSC / Swift code")

    # ── QR codes ───────────────────────────────────────────────────────────
    qr_code_1  = models.ImageField(upload_to="partner/", null=True, blank=True,
                                   help_text="QR Code for Bank 1 (e.g. ICICI)")
    qr_code_2  = models.ImageField(upload_to="partner/", null=True, blank=True,
                                   help_text="QR Code for Bank 2 (e.g. SBI)")

    # ── Misc ───────────────────────────────────────────────────────────────
    cheque_name = models.CharField(max_length=300, blank=True,
                                   default="Muhammadiyyah Educational & Social Welfare Trust",
                                   help_text="Name to write on cheques")
    tax_note   = models.CharField(max_length=300, blank=True, default="Tax Benefit: Applied For")
    is_active  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Be A Partner Page"
        verbose_name_plural = "Be A Partner Page"

    def __str__(self):
        return "Be A Partner Page"


class Maraji(models.Model):
    """
    A Shia Marja-e-Taqlid (Source of Emulation) whose spiritual authority
    is recognised by Madrasah Madinatul Ilm.

    Displayed as a full-bleed hero banner on the homepage.
    All text fields have 4-language variants (EN / AR / UR / FA) so the
    front-end language switcher can render the correct script and direction.

    is_deceased  : If True the banner renders the scholar's name with
                   "Rahmatullahi ʿAlayh" / رحمة الله عليه  rather than
                   the honourifics used for living maraji (dāma ẓilluhū).
    is_active    : Controls visibility on the homepage.
    sort_order   : When multiple maraji are active the one with the lowest
                   sort_order is displayed first (future-proof for a list).
    """

    # ── Photo ──────────────────────────────────────────────────────────────
    photo = models.ImageField(
        upload_to="maraji/",
        null=True, blank=True,
        help_text="Portrait photograph of the Marja — uploaded via admin. "
                  "Appears in the homepage hero banner."
    )

    # ── Names (4 languages) ────────────────────────────────────────────────
    name_en = models.CharField(max_length=200, help_text="English / transliterated name")
    name_ar = models.CharField(max_length=200, blank=True, help_text="Full Arabic name (calligraphic form)")
    name_ur = models.CharField(max_length=200, blank=True, help_text="Urdu name")
    name_fa = models.CharField(max_length=200, blank=True, help_text="Persian / Farsi name")

    # ── Primary honorific title (4 languages) ─────────────────────────────
    # e.g. "Hujjat ul-Islām wal Muslimīn" / "حجة الإسلام والمسلمين"
    title_en = models.CharField(max_length=300, blank=True)
    title_ar = models.CharField(max_length=300, blank=True)
    title_ur = models.CharField(max_length=300, blank=True)
    title_fa = models.CharField(max_length=300, blank=True)

    # ── Secondary title / role (4 languages) ──────────────────────────────
    # e.g. "Marjaʿ-e-Taqlīd · India" / "مرجع التقليد — الهند"
    role_en = models.CharField(max_length=300, blank=True)
    role_ar = models.CharField(max_length=300, blank=True)
    role_ur = models.CharField(max_length=300, blank=True)
    role_fa = models.CharField(max_length=300, blank=True)

    # ── Short description shown on homepage banner (4 languages) ──────────
    description_en = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)
    description_ur = models.TextField(blank=True)
    description_fa = models.TextField(blank=True)

    # ── Affiliation note (4 languages) ────────────────────────────────────
    # e.g. "Madrasah Madinatul Ilm operates under the spiritual guidance of…"
    affiliation_en = models.TextField(blank=True)
    affiliation_ar = models.TextField(blank=True)
    affiliation_ur = models.TextField(blank=True)
    affiliation_fa = models.TextField(blank=True)

    # ── Deceased flag ──────────────────────────────────────────────────────
    # When True: show "Rahmatullahi ʿAlayh" (رحمة الله عليه) instead of
    # the living honorific "Dāma Ẓilluhū" (دام ظله الوارف).
    is_deceased = models.BooleanField(
        default=False,
        verbose_name="Deceased (Rahmatullahi ʿAlayh)",
        help_text="Check this if the scholar has passed away. The banner will "
                  "display رحمة الله عليه instead of دام ظله الوارف."
    )
    date_of_passing = models.DateField(
        null=True, blank=True,
        help_text="Optional — date of passing, displayed if deceased."
    )

    # ── Display controls ───────────────────────────────────────────────────
    is_active  = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Marjaʿ"
        verbose_name_plural = "Marājiʿ (Spiritual Authorities)"
        ordering            = ["sort_order", "name_en"]

    def __str__(self):
        suffix = " (رحمة الله عليه)" if self.is_deceased else " (دام ظله)"
        return self.name_en + suffix

    @property
    def honorific_ar(self):
        """Returns the correct Arabic honorific based on deceased status."""
        return "رحمة الله عليه" if self.is_deceased else "دام ظله الوارف"

    @property
    def honorific_en(self):
        return "Rahmatullāhi ʿAlayh" if self.is_deceased else "Dāma Ẓilluhū l-ʿĀlī"

    @property
    def honorific_ur(self):
        return "رحمۃ اللہ علیہ" if self.is_deceased else "دام ظلہ العالی"

    @property
    def honorific_fa(self):
        return "رحمت‌الله علیه" if self.is_deceased else "دام ظله العالی"


class HeroBannerImage(models.Model):
    """
    Images that rotate in the hero banner background.
    Add/remove/reorder from Admin → Core → Hero Banner Images.
    At least one active image should always be present; the static
    banner.jpeg is used as a CSS fallback if no images are available.
    """
    image      = models.ImageField(
        upload_to="hero_banner/",
        help_text="Landscape image works best (min 1600×900 px). JPEG/WebP recommended."
    )
    caption    = models.CharField(max_length=200, blank=True,
                                  help_text="Optional internal caption (not shown on site).")
    is_active  = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0,
                                                  help_text="Lower number = shown first.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Hero Banner Image"
        verbose_name_plural = "Hero Banner Images"
        ordering            = ["sort_order", "uploaded_at"]

    def __str__(self):
        return self.caption or f"Hero image #{self.pk}"


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
