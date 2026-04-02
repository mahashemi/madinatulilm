"""
Contact & Q&A app models — with gender and country fields
"""
from django.db import models


GENDER_CHOICES = [
    ("",        "— Select Gender —"),
    ("male",    "Male"),
    ("female",  "Female"),
    ("other",   "Prefer not to say"),
]

# Comprehensive country list (ISO-ordered, common ones first)
COUNTRY_CHOICES = [
    ("",   "— Select Country —"),
    ("IN", "India"),
    ("PK", "Pakistan"),
    ("BD", "Bangladesh"),
    ("IQ", "Iraq"),
    ("IR", "Iran"),
    ("SA", "Saudi Arabia"),
    ("AE", "United Arab Emirates"),
    ("KW", "Kuwait"),
    ("QA", "Qatar"),
    ("BH", "Bahrain"),
    ("OM", "Oman"),
    ("US", "United States"),
    ("GB", "United Kingdom"),
    ("CA", "Canada"),
    ("AU", "Australia"),
    ("DE", "Germany"),
    ("FR", "France"),
    ("NL", "Netherlands"),
    ("SE", "Sweden"),
    ("NO", "Norway"),
    ("MY", "Malaysia"),
    ("ID", "Indonesia"),
    ("TR", "Turkey"),
    ("EG", "Egypt"),
    ("LB", "Lebanon"),
    ("SY", "Syria"),
    ("JO", "Jordan"),
    ("AF", "Afghanistan"),
    ("NP", "Nepal"),
    ("LK", "Sri Lanka"),
    ("NG", "Nigeria"),
    ("TZ", "Tanzania"),
    ("KE", "Kenya"),
    ("ZA", "South Africa"),
    ("BR", "Brazil"),
    ("AR", "Argentina"),
    ("MX", "Mexico"),
    ("JP", "Japan"),
    ("CN", "China"),
    ("RU", "Russia"),
    ("other", "Other"),
]


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ("new",      "New"),
        ("read",     "Read"),
        ("replied",  "Replied"),
        ("archived", "Archived"),
    ]
    full_name    = models.CharField(max_length=200)
    email        = models.EmailField()
    phone        = models.CharField(max_length=30, blank=True)
    gender       = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, default="")
    country      = models.CharField(max_length=10, choices=COUNTRY_CHOICES, blank=True, default="")
    subject      = models.CharField(max_length=300)
    message      = models.TextField()
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")
    admin_notes  = models.TextField(blank=True)
    ip_address   = models.GenericIPAddressField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.subject}"


class Question(models.Model):
    QUESTION_CATEGORY = [
        ("fiqh",    "Fiqh (Jurisprudence)"),
        ("aqeedah", "ʿAqīdah (Creed)"),
        ("akhlaq",  "Akhlāq (Ethics)"),
        ("quran",   "Qurʾān"),
        ("hadith",  "Hadith"),
        ("general", "General Islamic"),
        ("other",   "Other"),
    ]
    STATUS_CHOICES = [
        ("pending",  "Pending"),
        ("answered", "Answered"),
        ("rejected", "Rejected"),
    ]
    full_name    = models.CharField(max_length=200)
    email        = models.EmailField()
    phone        = models.CharField(max_length=30, blank=True)
    gender       = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, default="")
    country      = models.CharField(max_length=10, choices=COUNTRY_CHOICES, blank=True, default="")
    category     = models.CharField(max_length=20, choices=QUESTION_CATEGORY, default="general")
    question     = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    is_public    = models.BooleanField(default=False, help_text="Show question and answer publicly?")
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    answered_by  = models.CharField(max_length=200, blank=True)
    answer       = models.TextField(blank=True)
    answer_date  = models.DateTimeField(null=True, blank=True)
    ip_address   = models.GenericIPAddressField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.get_category_display()} [{self.status}]"
