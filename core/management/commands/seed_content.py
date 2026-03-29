"""
Management command: python manage.py seed_content
Seeds all initial content from the MohammadiyahTrust source documents.
Safe to run multiple times — uses get_or_create throughout.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
import datetime

from core.models import (
    SiteSettings, WelcomeSection, MissionSection, VisionSection,
    AboutSection, Founder, Trustee, AcademicProgram
)
from announcements.models import AnnouncementCategory
from lessons.models import Subject
from books.models import BookCategory
from sharia.models import ShariaCategory


class Command(BaseCommand):
    help = "Seed initial content from MohammadiyahTrust source documents"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("\n── Seeding Madrasah Madinatul Ilm content ──\n"))

        self._seed_site_settings()
        self._seed_welcome()
        self._seed_mission()
        self._seed_vision()
        self._seed_about()
        self._seed_founder()
        self._seed_trustees()
        self._seed_ijazat()
        self._seed_academic_programs()
        self._seed_subjects()
        self._seed_announcement_categories()
        self._seed_book_categories()
        self._seed_sharia_categories()

        self.stdout.write(self.style.SUCCESS("\n✅  All content seeded successfully!\n"))
        self.stdout.write("  → Visit http://127.0.0.1:8000 to see the website")
        self.stdout.write("  → Visit http://127.0.0.1:8000/admin to manage content\n")

    # ── Site Settings ──────────────────────────────────────────────────────
    def _seed_site_settings(self):
        obj, created = SiteSettings.objects.get_or_create(
            id=1,
            defaults=dict(
                site_name_en="Madrasah Madinatul Ilm",
                site_name_ar="مدرسة مدينة العلم",
                site_name_ur="مدرسہ مدینۃ العلم",
                tagline_en="Centre of Fiqāhat",
                trust_name="Muhammadiyah Trust",
                established=datetime.date(2026, 2, 3),
                address=(
                    "Madrasa Madinatul Ilm, Gopal Pur,\n"
                    "Post: Baqir Ganj, Thana: Hussain Ganj,\n"
                    "District: Siwan, Bihar — 841286"
                ),
                phone_primary="+91 8828073319",
                phone_secondary="+98 9055171993",
            )
        )
        self._log("SiteSettings", created)

    # ── Welcome ────────────────────────────────────────────────────────────
    def _seed_welcome(self):
        obj, created = WelcomeSection.objects.get_or_create(
            title_en="Welcome to Madrasah Madinatul Ilm",
            defaults=dict(
                title_ar="مرحباً بكم في مدرسة مدينة العلم",
                body_en=(
                    "<p>Welcome to the jurisprudence centre <strong>Madrasah Madinatul Ilm</strong>.</p>"
                    "<p>Madrasah Madinatul Ilm is dedicated to the dissemination of Islamic knowledge, "
                    "with a distinct mission to establish India as a center of advanced Islamic jurisprudence "
                    "(Fuqahat). We provide high-quality education and character development for those seeking "
                    "both knowledge and moral excellence.</p>"
                    "<p><strong>Muhammadiyah Trust</strong> is a religious and social organization whose aim "
                    "is to promote religious and worldly education, and to serve humanity in religious, "
                    "educational, and social fields with a spirit of human compassion, without discrimination "
                    "of religion or community.</p>"
                    "<p>Under the supervision of Muhammadiyah Trust, the Center of Fiqāhat Madrasa "
                    "Madinat-ul-Ilm was inaugurated on <strong>14 Sha'ban 1447 AH</strong>, corresponding to "
                    "<strong>3 February 2026</strong>, at Gopalpur, Siwan, Bihar.</p>"
                ),
                is_active=True,
            )
        )
        self._log("WelcomeSection", created)

    # ── Mission ────────────────────────────────────────────────────────────
    def _seed_mission(self):
        obj, created = MissionSection.objects.get_or_create(
            title_en="Our Mission",
            defaults=dict(
                body_en=(
                    "<p>We are committed to providing our students with an integrated and comprehensive "
                    "education. This encompasses core Islamic sciences such as <strong>Tafsir, Hadith, Fiqh, "
                    "Usul al-Fiqh, Aqeedah, and Rijal</strong>, complemented by a strong emphasis on ethical "
                    "integrity and advanced proficiency in Arabic, Persian, and English languages.</p>"
                    "<p>Our curriculum is a blend of classical Islamic knowledge and modern pedagogical "
                    "methods, designed to foster intellectual curiosity, responsible leadership, and a passion "
                    "for lifelong learning. The institution stands as a beacon of light, equipping students to "
                    "embody unity and compassion and to contribute constructively to society.</p>"
                    "<p>Madrasah Madinatul Ilm believes in a holistic approach to Islamic education, where "
                    "tradition is thoughtfully reconciled with contemporary understanding. We strive to develop "
                    "scholars and leaders who possess deep mastery of the Quran, Hadith, and Islamic sciences, "
                    "alongside the capability to address modern challenges effectively.</p>"
                ),
                is_active=True,
            )
        )
        self._log("MissionSection", created)

    # ── Vision ─────────────────────────────────────────────────────────────
    def _seed_vision(self):
        obj, created = VisionSection.objects.get_or_create(
            title_en="Our Vision",
            defaults=dict(
                body_en=(
                    "<p>Madrasah Madinatul Ilm envisions itself as a distinguished institution dedicated to "
                    "nurturing a deep, transformative understanding of faith across generations. We are "
                    "committed to cultivating scholars imbued with wisdom, profound juristic insight, and high "
                    "moral character, empowering them to guide and reform society.</p>"
                    "<p>We aspire towards a future where our graduates become exemplars in jurisprudence, "
                    "education, and moral guidance. Our philosophy is to maintain a deep-rooted connection "
                    "with Islamic heritage while harmoniously engaging with contemporary demands.</p>"
                    "<p>Our objective is to instill in a new generation a broad and profound comprehension of "
                    "Islamic teachings, producing individuals who are not only specialists in religious sciences "
                    "but also proactive in establishing harmony and justice within society.</p>"
                ),
                is_active=True,
            )
        )
        self._log("VisionSection", created)

    # ── About ──────────────────────────────────────────────────────────────
    def _seed_about(self):
        obj, created = AboutSection.objects.get_or_create(
            title_en="About Us",
            defaults=dict(
                body_en=(
                    "<p>Established in <strong>2026</strong> in Gopalpur, Madrasah Madinatul Ilm is a premier "
                    "Shia Islamic seminary in India, committed to advancing the legacy of knowledge, ethics, "
                    "and Islamic civilization. Our curriculum is meticulously designed to nurture generations "
                    "of scholars who possess deep faith, knowledge-in-action, and a passion for serving "
                    "creation.</p>"
                    "<p>Our mission is to embrace educational advancement while preserving the ancient Hawzah "
                    "tradition, inspiring students to serve humanity with knowledge, wisdom, and integrity, "
                    "and to champion the causes of compassion and human welfare.</p>"
                    "<p><strong>Muhammadiyah Trust</strong> — the governing trust — aims to promote religious "
                    "and worldly education without discrimination of religion or community, so that the "
                    "institution may also play its role in taking India to greater heights. Future plans include "
                    "schools, colleges, and hospitals for the general welfare of society.</p>"
                ),
                is_active=True,
            )
        )
        self._log("AboutSection", created)

    # ── Founder ────────────────────────────────────────────────────────────
    def _seed_founder(self):
        obj, created = Founder.objects.get_or_create(
            name_en="Syed Minhal Hussain Rizvi",
            defaults=dict(
                name_ar="السید منہال حسین رضوی",
                name_ur="احقر العباد السید منہال حسین گوپالپوری",
                title_en="Founder & Principal — Centre of Fiqāhat, Madrasah Madinatul Ilm",
                phone="+91 8828073319 | +98 9055171993",
                biography_ur=(
                    "<h4>باسمہ تعالی</h4>"
                    "<h5>اجمالی سوانح حیات</h5>"
                    "<p>احقر الزمن السید جواد عسکری الرضوی منہال گوپالپوری ابن مرحوم سید فخر العباد</p>"

                    "<p>حقیر بتاریخ <strong>14 اکتوبر سنہ 1990ء</strong> کو موضع گوپالپور، ضلع سیوان، "
                    "بہار میں آیۃ اللہ العظمی السید راحت حسین ہندی گوپالپوری کے دولت کدے میں پیدا ہوا۔</p>"

                    "<h5>خواب اور دینی تعلیم کا آغاز</h5>"
                    "<p>تقریبا 10 یا 11 سال کی عمر میں خود کو مسلسل خواب میں لباس روحانیت کی مخصوص ردا "
                    "اوڑھ کے پرواز کرتے دیکھتا تھا، جس کے بعد دینی تعلیم کی طرف رغبت ہوئی۔</p>"

                    "<h5>تعلیمی سفر</h5>"
                    "<ul>"
                    "<li>مدرسہ اسلامیہ کجھوہ — ابتدائی دینی تعلیم</li>"
                    "<li>حوزہ علمیہ امام محمد باقر علیہ السلام، بھیونڈی</li>"
                    "<li>حوزة المہدی، حیدر آباد</li>"
                    "<li>حوزہ علمیہ امیر المؤمنین علیہ السلام نجفی ہاؤس، ممبئی</li>"
                    "<li>مدرسہ امام خمینی رح، قم — کارشناسی (شیعہ شناسی)</li>"
                    "<li>مدرسہ عالی فقہ و اصول اسلامی «مدرسہ حجتیہ»، قم — کارشناسی ارشد (فقہ و اصول)</li>"
                    "</ul>"

                    "<h5>اجازات نقل روایت</h5>"
                    "<ul>"
                    "<li>آیة الله احمد کلباسی دام ظلہ</li>"
                    "<li>آیة الله سید کاظم مصطفوی دام ظلہ (شاگرد آیة الله العظمی السید الخوئی)</li>"
                    "<li>آیة الله العظمی شیخ ناصر مکارم شیرازی دام ظلہ</li>"
                    "<li>آیة الله العظمی شیخ جعفر سبحانی دام ظلہ</li>"
                    "</ul>"

                    "<h5>اجازات وکالت و صرف سہم امام و سادات</h5>"
                    "<ul>"
                    "<li>آیة الله سید کاظم مصطفوی دام ظلہ</li>"
                    "<li>آیة الله العظمی شیخ ناصر مکارم شیرازی دام ظلہ</li>"
                    "<li>آیة الله العظمی سید موسی شبیری زنجانی دام ظلہ</li>"
                    "<li>آیة الله العظمی السید علی حسینی السیستانی دام ظلہ</li>"
                    "</ul>"

                    "<p><em>و ما علینا الا البلاغ — والسلام علیکم</em></p>"
                    "<p><strong>احقر العباد السید منہال حسین گوپالپوری</strong><br>"
                    "11 فروری 2026ء بمطابق 22 شعبان 1447ھ</p>"
                ),
                biography_en=(
                    "<h4>In the Name of Allah</h4>"
                    "<h5>Brief Biography</h5>"
                    "<p>Born on <strong>14 October 1990</strong> in Gopalpur, District Siwan, Bihar, India — "
                    "in the household of Āyatullāh al-ʿUẓmā Syed Rahat Hussain Hindi Gopalpuri.</p>"

                    "<h5>Educational Journey</h5>"
                    "<ul>"
                    "<li>Madrasah Islamiyah Kajhwa — initial religious education</li>"
                    "<li>Hawzah Ilmiyyah Imam Muhammad Baqir (AS), Bhiwandi — Saraf, Nahw, Mantiq, Usul</li>"
                    "<li>Hawzat al-Mahdi, Hyderabad — Fiqh & advanced Nahw</li>"
                    "<li>Hawzah Ilmiyyah Amir al-Momineen (AS) — Najafi House, Mumbai — Lum'atayn, Usul</li>"
                    "<li>Madrasah Imam Khomeini (ra), Qom — BA in Shia Studies (Karshenasi)</li>"
                    "<li>Madrasah Hujjatiyyah, Qom — MA in Fiqh & Usul (Karshenasi Arshad) — "
                    "studying Kafayat al-Usul under <em>Āyatullāh Syed Nasir al-Din Hussaini</em> "
                    "and Makasib under <em>Āyatullāh Sheikh Muhammad Kazim Elahi</em>. Currently attending "
                    "Dars-e-Kharij of <em>Āyatullāh al-ʿUẓmā Sheikh Muhammad Mahdi Ganji</em>.</li>"
                    "</ul>"

                    "<h5>Scholarly Certifications (Ijāzāt)</h5>"
                    "<p><strong>Ijāzat Naql Riwāyat</strong> from:</p>"
                    "<ul>"
                    "<li>Āyatullāh Ahmad Kalbasi (descendant of Malik al-Ashtar)</li>"
                    "<li>Āyatullāh Syed Kazim Mustafawi (student of Āyatullāh al-ʿUẓmā al-Khoei)</li>"
                    "<li>Āyatullāh al-ʿUẓmā Sheikh Nasir Makarem Shirazi</li>"
                    "<li>Āyatullāh al-ʿUẓmā Sheikh Jafar Subhani</li>"
                    "</ul>"
                    "<p><strong>Ijāzat Wakalat & Sahm-e-Imam</strong> from:</p>"
                    "<ul>"
                    "<li>Āyatullāh Syed Kazim Mustafawi</li>"
                    "<li>Āyatullāh al-ʿUẓmā Sheikh Nasir Makarem Shirazi</li>"
                    "<li>Āyatullāh al-ʿUẓmā Syed Musa Shubayri Zanjani</li>"
                    "<li>Āyatullāh al-ʿUẓmā Syed Ali Hussaini Sistani</li>"
                    "</ul>"
                ),
                is_active=True,
                sort_order=1,
            )
        )
        self._log("Founder (Syed Minhal Hussain Rizvi)", created)

    # ── Trustees ───────────────────────────────────────────────────────────
    def _seed_trustees(self):
        from django.core.files import File
        import os

        trustees = [
            dict(name="Syed Minhal Hussain Rizvi",    designation="Principal & Founder — Centre of Fiqāhat",          phone="+91 8828073319", sort_order=1, photo_file="minhal.jpg"),
            dict(name="Maulana Syed Javed Akhtar",    designation="Vice Principal — Imam Juma wa Jama'at, Gopalpur",  phone="+91 9973559812", sort_order=2, photo_file="javed_akhtar.jpg"),
            dict(name="Mohammad Feroz Hashemi",       designation="Treasurer & Trustee — Muhammadiyah Trust",         phone="+91 9702289112", sort_order=3, photo_file="mohammad_feroz_hashemi.jpg"),
            dict(name="Syed Abul Qasim",              designation="Trustee — Muhammadiyah Trust",                     phone="",              sort_order=4, photo_file="syed_abulqasim.jpg"),
            dict(name="Syed Ali Abbas",               designation="Trustee — Muhammadiyah Trust",                     phone="",              sort_order=5, photo_file="syed_ali_abbas.jpg"),
            dict(name="Syed Ehtesham Hussain",        designation="Trustee — Muhammadiyah Trust",                     phone="",              sort_order=6, photo_file="syed_ehtesham.jpg"),
            dict(name="Syed MD Rizvi",                designation="Trustee — Muhammadiyah Trust",                     phone="",              sort_order=7, photo_file="syed_md_rizvi.jpg"),
            dict(name="Syed MD Zahid",                designation="Trustee — Muhammadiyah Trust",                     phone="",              sort_order=8, photo_file="syed_md_zahid.jpg"),
            dict(name="Ibrahim Chacha",               designation="Trustee — Muhammadiyah Trust",                     phone="",              sort_order=9, photo_file="ibrahim_chacha.jpg"),
        ]
        media_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "media", "trustees")
        for t in trustees:
            photo_file = t.pop("photo_file")
            obj, created = Trustee.objects.get_or_create(name=t["name"], defaults={**t, "is_active": True})
            if obj.photo == "" or obj.photo is None or not obj.photo:
                photo_path = os.path.join(media_dir, photo_file)
                if os.path.exists(photo_path):
                    with open(photo_path, "rb") as f:
                        obj.photo.save(photo_file, File(f), save=True)
            self._log(f"Trustee: {t['name']}", created)

    # ── Ijazat ─────────────────────────────────────────────────────────────
    def _seed_ijazat(self):
        from django.core.files import File
        import os
        from core.models import Ijazah

        media_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "media", "ijazat")
        ijazat = [
            dict(title="Ijāzat Naql Riwāyat — Āyatullāh Ahmad Kalbasi",          from_scholar="Āyatullāh Ahmad Kalbasi",                ijazah_type="riwayat",   sort_order=1, photo_file="riwayat_kalbasi.jpg"),
            dict(title="Ijāzat Naql Riwāyat — Āyatullāh Syed Kazim Mustafawi",   from_scholar="Āyatullāh Syed Kazim Mustafawi",         ijazah_type="riwayat",   sort_order=2, photo_file="riwayat_mustafawi.jpg"),
            dict(title="Ijāzat Naql Riwāyat — Āyatullāh Nasir Makarem Shirazi",  from_scholar="Āyatullāh Nasir Makarem Shirazi",        ijazah_type="riwayat",   sort_order=3, photo_file="riwayat_makarem.jpg"),
            dict(title="Ijāzat Naql Riwāyat — Āyatullāh Jafar Subhani (p.1)",   from_scholar="Āyatullāh Sheikh Jafar Subhani",         ijazah_type="riwayat",   sort_order=4, photo_file="riwayat_subhani_p1.jpg"),
            dict(title="Ijāzat Naql Riwāyat — Āyatullāh Jafar Subhani (p.2)",   from_scholar="Āyatullāh Sheikh Jafar Subhani",         ijazah_type="riwayat",   sort_order=5, photo_file="riwayat_subhani_p2.jpg"),
            dict(title="Ijāzat Wakalat — Āyatullāh Syed Kazim Mustafawi",        from_scholar="Āyatullāh Syed Kazim Mustafawi",         ijazah_type="wakalat",   sort_order=6, photo_file="wakalat_mustafawi.jpg"),
            dict(title="Ijāzat Wakalat — Āyatullāh Nasir Makarem Shirazi",       from_scholar="Āyatullāh Nasir Makarem Shirazi",        ijazah_type="wakalat",   sort_order=7, photo_file="wakalat_makarem.jpg"),
            dict(title="Ijāzat Wakalat — Āyatullāh Syed Musa Shubayri Zanjani", from_scholar="Āyatullāh Syed Musa Shubayri Zanjani",   ijazah_type="wakalat",   sort_order=8, photo_file="wakalat_zanjani.jpg"),
            dict(title="Ijāzat Sahm-e-Imam — Āyatullāh Syed Ali Sistani",       from_scholar="Āyatullāh Syed Ali Hussaini Sistani",    ijazah_type="sahm_imam", sort_order=9, photo_file="sahm_sistani.jpg"),
        ]
        for ij in ijazat:
            photo_file = ij.pop("photo_file")
            obj, created = Ijazah.objects.get_or_create(title=ij["title"], defaults=ij)
            if not obj.image:
                photo_path = os.path.join(media_dir, photo_file)
                if os.path.exists(photo_path):
                    with open(photo_path, "rb") as f:
                        obj.image.save(photo_file, File(f), save=True)
            self._log(f"Ijazah: {ij['title'][:50]}", created)

    # ── Academic Programs ──────────────────────────────────────────────────
    def _seed_academic_programs(self):
        programs = [
            dict(subject="quran",    title_en="Qurʾān",                   title_ar="القرآن الكريم",       icon_class="fas fa-book-open",    sort_order=1),
            dict(subject="hadith",   title_en="Hadith",                   title_ar="علم الحديث",          icon_class="fas fa-scroll",       sort_order=2),
            dict(subject="fiqh",     title_en="Fiqh",                     title_ar="الفقه",               icon_class="fas fa-balance-scale",sort_order=3),
            dict(subject="usul",     title_en="Usūl al-Fiqh",             title_ar="أصول الفقه",          icon_class="fas fa-sitemap",      sort_order=4),
            dict(subject="kalam",    title_en="Kalām & ʿAqīdah",         title_ar="الكلام والعقيدة",      icon_class="fas fa-star-and-crescent", sort_order=5),
            dict(subject="akhlaq",   title_en="Akhlāq",                   title_ar="الأخلاق",             icon_class="fas fa-heart",        sort_order=6),
            dict(subject="rational", title_en="Rational Sciences",        title_ar="العلوم العقلية",       icon_class="fas fa-brain",        sort_order=7),
            dict(subject="language", title_en="Language & Literature",    title_ar="اللغة والأدب",         icon_class="fas fa-language",     sort_order=8),
        ]
        for p in programs:
            obj, created = AcademicProgram.objects.get_or_create(subject=p["subject"], defaults={**p, "is_active": True})
            self._log(f"AcademicProgram: {p['title_en']}", created)

    # ── Subjects (for Lessons) ─────────────────────────────────────────────
    def _seed_subjects(self):
        subjects = [
            dict(slug="tafsir",   title_en="Tafsir",                title_ar="التفسير",         icon_class="fas fa-book-open",    sort_order=1),
            dict(slug="hadith",   title_en="Hadith",                title_ar="علم الحديث",      icon_class="fas fa-scroll",       sort_order=2),
            dict(slug="fiqh",     title_en="Fiqh",                  title_ar="الفقه",           icon_class="fas fa-balance-scale",sort_order=3),
            dict(slug="usul",     title_en="Usul al-Fiqh",          title_ar="أصول الفقه",      icon_class="fas fa-sitemap",      sort_order=4),
            dict(slug="kalam",    title_en="Kalam & Aqeedah",       title_ar="الكلام",          icon_class="fas fa-star-and-crescent", sort_order=5),
            dict(slug="akhlaq",   title_en="Akhlaq",                title_ar="الأخلاق",         icon_class="fas fa-heart",        sort_order=6),
            dict(slug="rational", title_en="Rational Sciences",     title_ar="العلوم العقلية",   icon_class="fas fa-brain",        sort_order=7),
            dict(slug="arabic",   title_en="Arabic Literature",     title_ar="الأدب العربي",    icon_class="fas fa-language",     sort_order=8),
        ]
        for s in subjects:
            obj, created = Subject.objects.get_or_create(slug=s["slug"], defaults={**s, "is_active": True})
            self._log(f"Subject: {s['title_en']}", created)

    # ── Announcement Categories ────────────────────────────────────────────
    # AnnouncementCategory uses 'slug' with SLUG_CHOICES: statement, message, meeting
    def _seed_announcement_categories(self):
        cats = [
            dict(slug="statement", title_en="Statement",      title_ar="البيانات"),
            dict(slug="message",   title_en="Issued Message", title_ar="الرسائل الصادرة"),
            dict(slug="meeting",   title_en="Meeting",        title_ar="الاجتماعات"),
        ]
        for c in cats:
            obj, created = AnnouncementCategory.objects.get_or_create(
                slug=c["slug"],
                defaults={"title_en": c["title_en"], "title_ar": c["title_ar"]}
            )
            self._log(f"AnnouncementCategory: {c['title_en']}", created)

    # ── Book Categories ────────────────────────────────────────────────────
    # BookCategory uses CATEGORY_CHOICES slugs: tafsir_hadith, rijal, fiqh, usul, kalam, akhlaq, rational, arabic, misc
    def _seed_book_categories(self):
        cats = [
            dict(slug="tafsir_hadith", title_en="Tafsīr & Hadith",    sort_order=1),
            dict(slug="rijal",         title_en="Rijāl",               sort_order=2),
            dict(slug="fiqh",          title_en="Fiqh",                sort_order=3),
            dict(slug="usul",          title_en="Usūl al-Fiqh",        sort_order=4),
            dict(slug="kalam",         title_en="Kalām & ʿAqīdah",    sort_order=5),
            dict(slug="akhlaq",        title_en="Akhlāq",              sort_order=6),
            dict(slug="rational",      title_en="Rational Sciences",   sort_order=7),
            dict(slug="arabic",        title_en="Arabic Literature",   sort_order=8),
            dict(slug="misc",          title_en="Miscellaneous",       sort_order=9),
        ]
        for c in cats:
            obj, created = BookCategory.objects.get_or_create(
                slug=c["slug"],
                defaults={"title_en": c["title_en"], "sort_order": c["sort_order"]}
            )
            self._log(f"BookCategory: {c['title_en']}", created)

    # ── Sharia Categories ──────────────────────────────────────────────────
    # ShariaCategory uses 'name' field with CATEGORY_CHOICES: kalam, akhlaq, fiqh
    def _seed_sharia_categories(self):
        cats = [
            dict(name="kalam",  title_en="Kalām & ʿAqīdah", title_ar="الكلام والعقيدة"),
            dict(name="akhlaq", title_en="Akhlāq",           title_ar="الأخلاق"),
            dict(name="fiqh",   title_en="Fiqh",             title_ar="الفقه"),
        ]
        for c in cats:
            obj, created = ShariaCategory.objects.get_or_create(
                name=c["name"],
                defaults={"title_en": c["title_en"], "title_ar": c["title_ar"]}
            )
            self._log(f"ShariaCategory: {c['title_en']}", created)

    def _log(self, label, created):
        status = self.style.SUCCESS("  ✓ Created") if created else "  · Already exists"
        self.stdout.write(f"{status}: {label}")
