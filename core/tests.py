"""
Comprehensive test suite — Madrasah Madinatul Ilm
Covers: all page views, all API endpoints, 404/500 handling, URL resolution.

Key facts about the data model:
  - sharia:category  → ShariaCategory.name  (kwarg: name=)
  - announcements:category → AnnouncementCategory.slug (kwarg: slug=)
  - lessons:subject  → Subject.slug          (kwarg: slug=)
  - books:category   → BookCategory.slug     (kwarg: slug=)
  All these use get_object_or_404, so test fixtures must exist.

Run:  python manage.py test core --verbosity=2
"""
from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch

from sharia.models import ShariaCategory
from announcements.models import AnnouncementCategory
from lessons.models import Subject
from books.models import BookCategory


# ──────────────────────────────────────────────────────────
# SHARED FIXTURE SETUP
# ──────────────────────────────────────────────────────────
class BaseFixtures(TestCase):
    """Creates the minimum DB rows needed by get_object_or_404 views."""

    @classmethod
    def setUpTestData(cls):
        # Sharia categories (keyed by `name`)
        for name in ["fiqh", "kalam", "akhlaq"]:
            ShariaCategory.objects.get_or_create(name=name)

        # Announcement categories (keyed by `slug`)  — meeting replaced by event
        for slug in ["statement", "message", "event"]:
            AnnouncementCategory.objects.get_or_create(slug=slug)

        # Lesson subjects (keyed by `slug`, requires is_active=True)
        for slug in ["quran", "tafsir", "hadith", "fiqh", "usul", "kalam", "akhlaq", "rational", "language"]:
            Subject.objects.get_or_create(slug=slug, defaults={"is_active": True, "title_en": slug.title()})

        # Book categories (keyed by `slug`)
        for slug in ["tafsir_hadith", "rijal", "fiqh", "usul", "kalam", "akhlaq", "rational", "arabic", "misc"]:
            BookCategory.objects.get_or_create(slug=slug, defaults={"title_en": slug.replace("_", " ").title()})


# ──────────────────────────────────────────────────────────
# 1. CORE VIEWS
# ──────────────────────────────────────────────────────────
class CoreViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_200(self):
        r = self.client.get(reverse("core:home"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "core/home.html")

    def test_about_200(self):
        r = self.client.get(reverse("core:about"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "core/about.html")

    def test_founder_200(self):
        r = self.client.get(reverse("core:founder"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "core/founder.html")

    def test_academics_200(self):
        r = self.client.get(reverse("core:academics"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "core/academics.html")

    def test_gallery_200(self):
        r = self.client.get(reverse("core:gallery"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "core/gallery.html")

    def test_partner_200(self):
        r = self.client.get(reverse("core:partner"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "core/partner.html")

    def test_partner_has_donation_items(self):
        r = self.client.get(reverse("core:partner"))
        self.assertIn("donation_items", r.context)
        self.assertGreater(len(r.context["donation_items"]), 0)

    def test_home_has_hadiths_json(self):
        r = self.client.get(reverse("core:home"))
        self.assertIn("hadiths_json", r.context)


# ──────────────────────────────────────────────────────────
# 2. QURAN VIEWS
# ──────────────────────────────────────────────────────────
class QuranViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_quran_home_200(self):
        r = self.client.get(reverse("quran:home"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "quran_app/quran_home.html")

    def test_quran_detail_nonexistent_404(self):
        r = self.client.get("/quran/99999/")
        self.assertEqual(r.status_code, 404)


# ──────────────────────────────────────────────────────────
# 3. SHARIA VIEWS  (URL kwarg = name=, not slug=)
# ──────────────────────────────────────────────────────────
class ShariaViewTests(BaseFixtures):
    def setUp(self):
        self.client = Client()

    def _cat(self, name):
        # sharia URL pattern: path("<str:name>/", ..., name="category")
        return self.client.get(reverse("sharia:category", kwargs={"name": name}))

    def test_sharia_home_200(self):
        r = self.client.get(reverse("sharia:home"))
        self.assertEqual(r.status_code, 200)

    def test_sharia_fiqh_200(self):
        self.assertEqual(self._cat("fiqh").status_code, 200)

    def test_sharia_kalam_200(self):
        self.assertEqual(self._cat("kalam").status_code, 200)

    def test_sharia_akhlaq_200(self):
        self.assertEqual(self._cat("akhlaq").status_code, 200)

    def test_sharia_category_unknown_404(self):
        r = self._cat("nonexistent_xyz")
        self.assertEqual(r.status_code, 404)

    def test_sharia_detail_nonexistent_404(self):
        r = self.client.get("/sharia/detail/99999/")
        self.assertEqual(r.status_code, 404)


# ──────────────────────────────────────────────────────────
# 4. ANNOUNCEMENTS VIEWS
# ──────────────────────────────────────────────────────────
class AnnouncementsViewTests(BaseFixtures):
    def setUp(self):
        self.client = Client()

    def _cat(self, slug):
        return self.client.get(reverse("announcements:category", kwargs={"slug": slug}))

    def test_announcements_home_200(self):
        r = self.client.get(reverse("announcements:home"))
        self.assertEqual(r.status_code, 200)

    def test_statement_200(self):
        self.assertEqual(self._cat("statement").status_code, 200)

    def test_message_200(self):
        self.assertEqual(self._cat("message").status_code, 200)

    def test_event_200(self):
        self.assertEqual(self._cat("event").status_code, 200)

    def test_category_unknown_404(self):
        self.assertEqual(self._cat("nonexistent_xyz").status_code, 404)

    def test_announcement_detail_nonexistent_404(self):
        r = self.client.get("/announcements/detail/99999/")
        self.assertEqual(r.status_code, 404)


# ──────────────────────────────────────────────────────────
# 5. LESSONS VIEWS
# ──────────────────────────────────────────────────────────
class LessonsViewTests(BaseFixtures):
    SUBJECTS = ["tafsir", "hadith", "fiqh", "usul", "kalam", "akhlaq", "rational", "language"]

    def setUp(self):
        self.client = Client()

    def test_lessons_home_200(self):
        r = self.client.get(reverse("lessons:home"))
        self.assertEqual(r.status_code, 200)

    def test_all_subjects_200(self):
        for slug in self.SUBJECTS:
            with self.subTest(subject=slug):
                r = self.client.get(reverse("lessons:subject", kwargs={"slug": slug}))
                self.assertEqual(r.status_code, 200, msg=f"Subject '{slug}' returned {r.status_code}")

    def test_subject_unknown_404(self):
        r = self.client.get(reverse("lessons:subject", kwargs={"slug": "nonexistent_xyz"}))
        self.assertEqual(r.status_code, 404)

    def test_lesson_series_nonexistent_404(self):
        r = self.client.get("/lessons/series/99999/")
        self.assertEqual(r.status_code, 404)

    def test_lesson_detail_nonexistent_404(self):
        r = self.client.get("/lessons/lesson/99999/")
        self.assertEqual(r.status_code, 404)


# ──────────────────────────────────────────────────────────
# 6. BOOKS VIEWS
# ──────────────────────────────────────────────────────────
class BooksViewTests(BaseFixtures):
    CATEGORIES = [
        "tafsir_hadith", "rijal", "fiqh", "usul", "kalam",
        "akhlaq", "rational", "arabic", "misc",
    ]

    def setUp(self):
        self.client = Client()

    def test_books_home_200(self):
        r = self.client.get(reverse("books:home"))
        self.assertEqual(r.status_code, 200)

    def test_all_categories_200(self):
        for slug in self.CATEGORIES:
            with self.subTest(category=slug):
                r = self.client.get(reverse("books:category", kwargs={"slug": slug}))
                self.assertEqual(r.status_code, 200, msg=f"Category '{slug}' returned {r.status_code}")

    def test_category_unknown_404(self):
        r = self.client.get(reverse("books:category", kwargs={"slug": "nonexistent_xyz"}))
        self.assertEqual(r.status_code, 404)

    def test_book_detail_nonexistent_404(self):
        r = self.client.get("/books/99999/")
        self.assertEqual(r.status_code, 404)


# ──────────────────────────────────────────────────────────
# 7. CONTACT VIEWS
# ──────────────────────────────────────────────────────────
class ContactViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_200(self):
        r = self.client.get(reverse("contact:contact"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "contact/contact.html")

    def test_ask_200(self):
        r = self.client.get(reverse("contact:ask"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "contact/ask_question.html")

    def test_contact_post_valid(self):
        r = self.client.post(reverse("contact:contact"), {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test",
            "message": "Hello from test",
        })
        self.assertIn(r.status_code, [200, 302])
        self.assertNotEqual(r.status_code, 500)

    def test_ask_post_valid(self):
        r = self.client.post(reverse("contact:ask"), {
            "name": "Test User",
            "email": "test@example.com",
            "question": "What is the ruling on X?",
            "category": "fiqh",
        })
        self.assertIn(r.status_code, [200, 302])
        self.assertNotEqual(r.status_code, 500)


# ──────────────────────────────────────────────────────────
# 8. REST API ENDPOINTS
# ──────────────────────────────────────────────────────────
class APIEndpointTests(TestCase):
    def setUp(self):
        self.client = Client()

    def _get(self, path):
        return self.client.get(path, HTTP_ACCEPT="application/json")

    def test_api_quran_200(self):
        self.assertEqual(self._get("/api/v1/quran/").status_code, 200)

    def test_api_sharia_200(self):
        self.assertEqual(self._get("/api/v1/sharia/").status_code, 200)

    def test_api_announcements_200(self):
        self.assertEqual(self._get("/api/v1/announcements/").status_code, 200)

    def test_api_lessons_200(self):
        self.assertEqual(self._get("/api/v1/lessons/").status_code, 200)

    def test_api_books_200(self):
        self.assertEqual(self._get("/api/v1/books/").status_code, 200)

    def test_api_contact_200(self):
        self.assertEqual(self._get("/api/v1/contact/").status_code, 200)

    def test_api_core_not_500(self):
        r = self._get("/api/v1/")
        self.assertNotEqual(r.status_code, 500)

    def test_api_books_returns_json(self):
        r = self._get("/api/v1/books/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("application/json", r.get("Content-Type", ""))

    def test_api_nonexistent_404(self):
        self.assertEqual(self._get("/api/v1/nonexistent/").status_code, 404)


# ──────────────────────────────────────────────────────────
# 9. ERROR HANDLERS
# ──────────────────────────────────────────────────────────
class ErrorHandlerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_unknown_path_404(self):
        self.assertEqual(self.client.get("/this-page-does-not-exist-xyz/").status_code, 404)

    def test_admin_login_200(self):
        self.assertEqual(self.client.get("/admin/login/").status_code, 200)

    def test_static_css_not_500(self):
        r = self.client.get("/static/css/main.css")
        self.assertNotEqual(r.status_code, 500)


# ──────────────────────────────────────────────────────────
# 10. URL REVERSE RESOLUTION
# ──────────────────────────────────────────────────────────
class URLReverseTests(TestCase):
    """
    Verifies every named URL used in base.html and templates
    can be reversed without NoReverseMatch.
    Sharia uses kwarg `name=`, all others use `slug=`.
    """
    NAMED_URLS = [
        ("core:home",     {}),
        ("core:about",    {}),
        ("core:founder",  {}),
        ("core:academics",{}),
        ("core:gallery",  {}),
        ("core:partner",  {}),
        ("quran:home",    {}),
        # sharia uses name= kwarg
        ("sharia:home",   {}),
        ("sharia:category", {"name": "fiqh"}),
        ("sharia:category", {"name": "kalam"}),
        ("sharia:category", {"name": "akhlaq"}),
        # announcements uses slug= kwarg
        ("announcements:home", {}),
        ("announcements:category", {"slug": "statement"}),
        ("announcements:category", {"slug": "message"}),
        ("announcements:category", {"slug": "event"}),
        # lessons uses slug= kwarg
        ("lessons:home", {}),
        ("lessons:subject", {"slug": "tafsir"}),
        ("lessons:subject", {"slug": "hadith"}),
        ("lessons:subject", {"slug": "fiqh"}),
        ("lessons:subject", {"slug": "usul"}),
        ("lessons:subject", {"slug": "kalam"}),
        ("lessons:subject", {"slug": "akhlaq"}),
        ("lessons:subject", {"slug": "rational"}),
        ("lessons:subject", {"slug": "language"}),
        # books uses slug= kwarg
        ("books:home", {}),
        ("books:category", {"slug": "tafsir_hadith"}),
        ("books:category", {"slug": "fiqh"}),
        ("books:category", {"slug": "kalam"}),
        ("books:category", {"slug": "misc"}),
        # contact
        ("contact:contact", {}),
        ("contact:ask",     {}),
    ]

    def test_all_named_urls_resolve(self):
        for name, kwargs in self.NAMED_URLS:
            with self.subTest(url=name, kwargs=kwargs):
                try:
                    url = reverse(name, kwargs=kwargs)
                    self.assertIsNotNone(url)
                except NoReverseMatch as e:
                    self.fail(f"reverse('{name}', kwargs={kwargs}) raised NoReverseMatch: {e}")
