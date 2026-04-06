"""
Management command: seed_useful_links
Inserts curated Islamic resource links into the UsefulLink table.
Safe to run multiple times — uses get_or_create on URL.
"""
from django.core.management.base import BaseCommand
from books.models import UsefulLink


LINKS = [
    # ── Maraji Offices ────────────────────────────────────────
    dict(title="Office of Ayatollah Sistani",
         url="https://www.sistani.org",
         description="Official website of Grand Ayatollah Syed Ali al-Sistani",
         category="maraji", icon_class="fas fa-star-and-crescent", sort_order=1),
    dict(title="Office of Ayatollah Khamenei",
         url="https://www.khamenei.ir",
         description="Official site of Grand Ayatollah Syed Ali Khamenei",
         category="maraji", icon_class="fas fa-star-and-crescent", sort_order=2),
    dict(title="Office of Ayatollah Makarem Shirazi",
         url="https://www.makaremshirazi.org",
         description="Official website of Grand Ayatollah Nasir Makarim Shirazi",
         category="maraji", icon_class="fas fa-star-and-crescent", sort_order=3),
    dict(title="Al-Khoei Foundation",
         url="https://www.al-khoei.us",
         description="Legacy of Grand Ayatollah Abu'l-Qasim al-Khoei",
         category="maraji", icon_class="fas fa-star-and-crescent", sort_order=4),
    # ── Quran & Tafsir ────────────────────────────────────────
    dict(title="Quran.com",
         url="https://quran.com",
         description="Read, listen and study the Holy Quran with multiple tafsirs",
         category="quran", icon_class="fas fa-book-open", sort_order=1),
    dict(title="Al-Islam.org — Quran",
         url="https://www.al-islam.org/quran",
         description="Shia-perspective Quranic resources and translations",
         category="quran", icon_class="fas fa-book-open", sort_order=2),
    dict(title="Tanzil.net",
         url="https://tanzil.net",
         description="Accurate Quran Unicode text with multiple translations",
         category="quran", icon_class="fas fa-book-open", sort_order=3),
    # ── Hadith & Rijal ────────────────────────────────────────
    dict(title="Al-Islam.org — Hadith",
         url="https://www.al-islam.org/hadith",
         description="Shia Hadith collections — Kulayni, Majlisi, etc.",
         category="hadith", icon_class="fas fa-scroll", sort_order=1),
    dict(title="Shia Hadith Database",
         url="https://thaqalayn.net",
         description="Searchable database of Shia hadith with English translations",
         category="hadith", icon_class="fas fa-scroll", sort_order=2),
    # ── Dua & Ziyarat ─────────────────────────────────────────
    dict(title="Dua.org",
         url="https://www.dua.org",
         description="Comprehensive Shia supplications, ziyarat and amaal",
         category="dua", icon_class="fas fa-hands", sort_order=1),
    dict(title="Duas.org",
         url="https://www.duas.org",
         description="Duaas, ziyarats, namaaz and Islamic calendar",
         category="dua", icon_class="fas fa-hands", sort_order=2),
    dict(title="Ahlulbayt TV",
         url="https://www.ahlulbayt.tv",
         description="Live and on-demand Islamic programming including duas",
         category="dua", icon_class="fas fa-hands", sort_order=3),
    # ── Fiqh & Fatawa ─────────────────────────────────────────
    dict(title="Sistani — Practical Laws",
         url="https://www.sistani.org/english/book/48/",
         description="A Code of Practice for Muslims in the West",
         category="sharia", icon_class="fas fa-balance-scale", sort_order=1),
    dict(title="IslamQuest",
         url="https://www.islamquest.net",
         description="Shia fatawa and Q&A answered by maraji scholars",
         category="sharia", icon_class="fas fa-balance-scale", sort_order=2),
    # ── Islamic Education ─────────────────────────────────────
    dict(title="Hawza.net",
         url="https://www.hawza.net",
         description="Online Islamic seminary resources and courses",
         category="education", icon_class="fas fa-graduation-cap", sort_order=1),
    dict(title="IQNA — Islamic World News",
         url="https://www.iqna.ir/en",
         description="Islamic world news and educational resources from Qom",
         category="education", icon_class="fas fa-graduation-cap", sort_order=2),
    dict(title="Islamic College London",
         url="https://www.islamic-college.ac.uk",
         description="Degree-level Islamic studies and research",
         category="education", icon_class="fas fa-graduation-cap", sort_order=3),
    # ── Digital Libraries ─────────────────────────────────────
    dict(title="Al-Islam.org",
         url="https://www.al-islam.org",
         description="Largest online Shia Islamic library — books, articles, multimedia",
         category="library", icon_class="fas fa-book", sort_order=1),
    dict(title="Noor Digital Library",
         url="https://www.noorlib.ir",
         description="Extensive Arabic and Islamic manuscript digital library",
         category="library", icon_class="fas fa-book", sort_order=2),
    dict(title="Internet Archive — Islamic Texts",
         url="https://archive.org/search?query=shia+islamic",
         description="Free access to classical Islamic texts and manuscripts",
         category="library", icon_class="fas fa-book", sort_order=3),
]


class Command(BaseCommand):
    help = "Seed curated Islamic resource links into UsefulLink table"

    def handle(self, *args, **options):
        created_count = 0
        for data in LINKS:
            _, created = UsefulLink.objects.get_or_create(
                url=data["url"], defaults=data
            )
            if created:
                created_count += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Done: {created_count} new links added "
                f"({len(LINKS) - created_count} already existed)."
            )
        )
