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
        self._seed_ijazah()
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
                tagline_en="Centre of Faqāhat",
                trust_name="Muhammadiyah Trust",
                established=datetime.date(2026, 2, 3),
                address=(
                    "Madrasah Madinatul Ilm, Gopal Pur,\n"
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
        WELCOME_DATA = dict(
            title_ar="مرحباً بكم في مدرسة مدينة العلم",
            title_ur="مدرسہ مدینۃ العلم میں خوش آمدید",
            title_fa="خوش آمدید به مدرسه مدینةالعلم",
            body_en=(
                    "<p>Welcome to the jurisprudence centre <strong>Madrasah Madinatul Ilm</strong>.</p>"
                    "<p>Madrasah Madinatul Ilm is dedicated to the dissemination of Islamic knowledge, "
                    "with a distinct mission to establish India as a center of advanced Islamic jurisprudence "
                    "(Faqahat). We provide high-quality education and character development for those seeking "
                    "both knowledge and moral excellence.</p>"
                    "<p><strong>Muhammadiyah Trust</strong> is a religious and social organization whose aim "
                    "is to promote religious and worldly education, and to serve humanity in religious, "
                    "educational, and social fields with a spirit of human compassion, without discrimination "
                    "of religion or community.</p>"
                    "<p>Under the supervision of Muhammadiyah Trust, the Center of Faqāhat - Madrasah "
                    "Madinat-ul-Ilm was inaugurated on <strong>14 Sha'ban 1447 AH</strong>, corresponding to "
                    "<strong>3 February 2026</strong>, at Gopalpur, Siwan, Bihar.</p>"
                ),
            body_ar=(
                "<p>مرحباً بكم في مركز الفقاهة <strong>مدرسة مدينة العلم</strong>.</p>"
                "<p>تكرّس مدرسة مدينة العلم جهودها لنشر المعرفة الإسلامية، بمهمة واضحة لجعل "
                "الهند مركزاً للفقه الإسلامي المتقدم. نقدم تعليماً راقياً وتنمية للشخصية لمن "
                "يسعون إلى العلم والفضيلة معاً.</p>"
                "<p>تأسست المدرسة تحت إشراف <strong>مؤسسة محمدية</strong> بتاريخ "
                "<strong>١٤ شعبان ١٤٤٧ هـ</strong> الموافق <strong>٣ فبراير ٢٠٢٦</strong> "
                "في قرية گوپالپور، سيوان، بيهار.</p>"
            ),
            body_ur=(
                "<p>فقاہت کے مرکز <strong>مدرسہ مدینۃ العلم</strong> میں خوش آمدید۔</p>"
                "<p>مدرسہ مدینۃ العلم اسلامی علوم کی ترویج کے لیے وقف ہے، جس کا خاص مشن ہندوستان کو "
                "اعلیٰ اسلامی فقاہت کا مرکز بنانا ہے۔ ہم علم اور اخلاق دونوں کے طالبین کے لیے "
                "اعلیٰ معیار کی تعلیم اور کردار سازی فراہم کرتے ہیں۔</p>"
                "<p><strong>محمدیہ ٹرسٹ</strong> کی نگرانی میں مرکزِ فقاہت مدرسہ مدینۃ العلم کا "
                "افتتاح <strong>۱۴ شعبان ۱۴۴۷ھ</strong> بمطابق <strong>۳ فروری ۲۰۲۶ء</strong> "
                "کو گوپالپور، سیوان، بہار میں ہوا۔</p>"
            ),
            body_fa=(
                "<p>به مرکز فقاهت <strong>مدرسه مدینةالعلم</strong> خوش آمدید.</p>"
                "<p>مدرسه مدینةالعلم در خدمت نشر علوم اسلامی است و مأموریت ویژه‌ای دارد: "
                "تبدیل هند به مرکز فقه اسلامی پیشرفته. ما آموزش باکیفیت و تربیت اخلاقی را "
                "برای طالبان علم و فضیلت فراهم می‌کنیم.</p>"
                "<p>این مدرسه زیر نظر <strong>موقوفه محمدیه</strong> در تاریخ "
                "<strong>۱۴ شعبان ۱۴۴۷ هـ</strong> برابر با <strong>۳ فوریه ۲۰۲۶</strong> "
                "در گوپال‌پور، سیوان، بیهار افتتاح شد.</p>"
            ),
            is_active=True,
        )
        obj, created = WelcomeSection.objects.update_or_create(
            title_en="Welcome to Madrasah Madinatul Ilm",
            defaults=WELCOME_DATA,
        )
        self._log("WelcomeSection", created)

    # ── Mission ────────────────────────────────────────────────────────────
    def _seed_mission(self):
        MISSION_DATA = dict(
            title_ar="مهمتنا",
            title_ur="ہمارا مشن",
            title_fa="مأموریت ما",
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
            body_ar=(
                "<p>نلتزم بتزويد طلابنا بتعليم متكامل وشامل يشمل العلوم الإسلامية الأساسية "
                "كالتفسير والحديث والفقه وأصول الفقه والعقيدة وعلم الرجال، مع التركيز على "
                "النزاهة الأخلاقية والإتقان المتقدم للغات العربية والفارسية والإنجليزية.</p>"
                "<p>منهجنا الدراسي يجمع بين المعرفة الإسلامية الكلاسيكية والأساليب التربوية "
                "الحديثة، بهدف تنمية الفضول الفكري والقيادة المسؤولة والشغف بالتعلم المستمر.</p>"
            ),
            body_ur=(
                "<p>ہم اپنے طلباء کو ایک مکمل اور جامع تعلیم فراہم کرنے کے پابند ہیں جس میں "
                "تفسیر، حدیث، فقہ، اصول الفقہ، عقیدہ اور رجال جیسے بنیادی اسلامی علوم شامل ہیں، "
                "ساتھ ہی عربی، فارسی اور انگریزی زبانوں میں اعلیٰ مہارت پر خصوصی توجہ دی جاتی ہے۔</p>"
                "<p>ہمارا نصاب کلاسیکی اسلامی علم اور جدید تدریسی طریقوں کا امتزاج ہے جو فکری "
                "تجسس، ذمہ دار قیادت اور تاحیات سیکھنے کے جذبے کو فروغ دینے کے لیے ڈیزائن کیا گیا ہے۔</p>"
            ),
            body_fa=(
                "<p>ما متعهدیم که آموزشی یکپارچه و جامع به دانش‌آموزان خود ارائه دهیم که علوم "
                "اسلامی اصلی مانند تفسیر، حدیث، فقه، اصول فقه، عقیده و رجال را دربرمی‌گیرد، "
                "همراه با تأکید قوی بر صداقت اخلاقی و تسلط پیشرفته بر زبان‌های عربی، فارسی و انگلیسی.</p>"
                "<p>برنامه درسی ما ترکیبی از دانش کلاسیک اسلامی و روش‌های آموزشی مدرن است که برای "
                "پرورش کنجکاوی فکری، رهبری مسئولانه و شور یادگیری مادام‌العمر طراحی شده است.</p>"
            ),
            is_active=True,
        )
        obj, created = MissionSection.objects.update_or_create(
            title_en="Our Mission",
            defaults=MISSION_DATA,
        )
        self._log("MissionSection", created)

    # ── Vision ─────────────────────────────────────────────────────────────
    def _seed_vision(self):
        VISION_DATA = dict(
            title_ar="رؤيتنا",
            title_ur="ہمارا وژن",
            title_fa="چشم‌انداز ما",
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
            body_ar=(
                "<p>ترى مدرسة مدينة العلم في نفسها مؤسسة متميزة مكرّسة لتنمية فهم عميق ومحوّل "
                "للإيمان عبر الأجيال. نسعى إلى تخريج علماء يتمتعون بالحكمة والبصيرة الفقهية "
                "العميقة والأخلاق الرفيعة، يقودون المجتمع ويُصلحونه.</p>"
                "<p>نطمح إلى مستقبل يصبح فيه خريجونا قدوةً في الفقه والتعليم والإرشاد الأخلاقي، "
                "محافظين على الروابط الراسخة مع التراث الإسلامي مع التعامل المنسجم مع متطلبات العصر.</p>"
            ),
            body_ur=(
                "<p>مدرسہ مدینۃ العلم اپنے آپ کو ایک ممتاز ادارے کے طور پر دیکھتا ہے جو نسل در نسل "
                "ایمان کی گہری اور تبدیلی آور سمجھ کو پروان چڑھانے کے لیے وقف ہے۔ ہم حکمت، "
                "گہری فقہی بصیرت اور اعلیٰ اخلاقی کردار سے مزین علماء تیار کرنے کے لیے پرعزم ہیں۔</p>"
                "<p>ہم ایسے مستقبل کی طرف گامزن ہیں جہاں ہمارے فارغین فقہ، تعلیم اور اخلاقی رہنمائی "
                "میں نمونہ بنیں، اسلامی ورثے سے گہری وابستگی برقرار رکھتے ہوئے عصری تقاضوں سے "
                "ہم آہنگی کے ساتھ نمٹیں۔</p>"
            ),
            body_fa=(
                "<p>مدرسه مدینةالعلم خود را به عنوان یک نهاد ممتاز می‌بیند که وقف پرورش درک عمیق "
                "و تحول‌آفرین از ایمان در میان نسل‌ها است. ما متعهدیم که عالمانی تربیت کنیم که "
                "دارای حکمت، بینش فقهی عمیق و شخصیت اخلاقی والا باشند.</p>"
                "<p>ما آرزو داریم آینده‌ای بسازیم که در آن فارغ‌التحصیلان ما الگویی در فقه، "
                "آموزش و راهنمایی اخلاقی باشند و ضمن حفظ پیوند ریشه‌دار با میراث اسلامی، "
                "با نیازهای معاصر هماهنگ باشند.</p>"
            ),
            is_active=True,
        )
        obj, created = VisionSection.objects.update_or_create(
            title_en="Our Vision",
            defaults=VISION_DATA,
        )
        self._log("VisionSection", created)

    # ── About ──────────────────────────────────────────────────────────────
    def _seed_about(self):
        obj, created = AboutSection.objects.update_or_create(
            title_en="About Us",
            defaults=dict(
                title_ar="من نحن",
                title_ur="ہمارے بارے میں",
                title_fa="درباره ما",
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
                body_ar=(
                    "<p>تأسست مدرسة مدينة العلم عام <strong>٢٠٢٦</strong> في قرية گوپالپور، "
                    "وهي إحدى أرقى المدارس الشيعية الإسلامية في الهند، تسعى إلى صون إرث "
                    "العلم والأخلاق والحضارة الإسلامية. يُصمَّم مناهجنا بعناية لتهيئة أجيال "
                    "من العلماء الذين يتحلّون بالإيمان العميق والعلم التطبيقي والشغف بخدمة الخلق.</p>"
                    "<p>مهمتنا هي تبنّي التقدم التعليمي مع الحفاظ على تقاليد الحوزة العلمية "
                    "العريقة، وإلهام الطلاب لخدمة الإنسانية بالعلم والحكمة والنزاهة، والدفاع "
                    "عن قضايا الرحمة والرفاه الإنساني.</p>"
                    "<p><strong>مؤسسة محمدية</strong> — الهيئة المشرفة — تهدف إلى تعزيز التعليم "
                    "الديني والدنيوي دون تمييز بين الأديان أو المجتمعات. وتشمل الخطط المستقبلية "
                    "إنشاء مدارس وجامعات ومستشفيات لخدمة المجتمع.</p>"
                ),
                body_ur=(
                    "<p>مدرسہ مدینۃ العلم <strong>2026ء</strong> میں گوپالپور میں قائم ہوا — "
                    "یہ ہندوستان کا ایک اہم شیعہ اسلامی علمی مرکز ہے جو علم، اخلاق اور "
                    "اسلامی تہذیب کی میراث کو آگے بڑھانے کے لیے پرعزم ہے۔ ہمارا نصاب ایسے "
                    "علماء کی نسلوں کی تربیت کے لیے مرتب کیا گیا ہے جو گہرے ایمان، عملی علم "
                    "اور مخلوق کی خدمت کے جذبے سے سرشار ہوں۔</p>"
                    "<p>ہمارا مشن یہ ہے کہ قدیم حوزوی روایت کو برقرار رکھتے ہوئے تعلیمی ترقی "
                    "کو اپنایا جائے، اور طلاب کو علم، حکمت اور دیانتداری کے ساتھ انسانیت کی "
                    "خدمت کے لیے تیار کیا جائے۔</p>"
                    "<p><strong>محمدیہ ٹرسٹ</strong> — یہ انتظامی ادارہ — بلا تفریق مذہب و ملت "
                    "دینی اور دنیاوی تعلیم کے فروغ کا ہدف رکھتا ہے۔ مستقبل کے منصوبوں میں "
                    "اسکول، کالج اور ہسپتال شامل ہیں۔</p>"
                ),
                body_fa=(
                    "<p>مدرسه مدینةالعلم در سال <strong>۲۰۲۶</strong> در گوپال‌پور تأسیس شد — "
                    "یکی از برجسته‌ترین حوزه‌های علمیه شیعی در هند که در تلاش برای پیشبرد "
                    "میراث علم، اخلاق و تمدن اسلامی است. برنامه درسی ما به دقت طراحی شده "
                    "تا نسل‌هایی از عالمان متقی، عامل به علم و خادم خلق تربیت کند.</p>"
                    "<p>مأموریت ما این است که با حفظ سنت دیرینه حوزوی، پیشرفت آموزشی را "
                    "در آغوش بگیریم و دانش‌آموزان را برای خدمت به انسانیت با علم، حکمت و "
                    "صداقت آماده سازیم.</p>"
                    "<p><strong>موقوفه محمدیه</strong> — هیئت مدیریتی — بدون تبعیض مذهبی یا "
                    "قومی به دنبال ترویج آموزش دینی و دنیوی است. برنامه‌های آینده شامل "
                    "مدارس، دانشگاه‌ها و بیمارستان‌ها برای رفاه عمومی جامعه است.</p>"
                ),
                is_active=True,
            )
        )
        self._log("AboutSection", created)

    # ── Founder ────────────────────────────────────────────────────────────
    def _seed_founder(self):
        obj, created = Founder.objects.update_or_create(
            name_en="Syed Minhal Hussain Rizvi",
            defaults=dict(
                name_ar="السيد منهال حسين رضوي",
                name_ur="احقر العباد السید منہال حسین گوپالپوری",
                title_en="Founder & Principal — Centre of Faqāhat, Madrasah Madinatul Ilm",
                phone="+91 8828073319 | +98 9055171993",

                # ── Urdu Biography ─────────────────────────────────────────
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

                # ── English Biography ──────────────────────────────────────
                biography_en=(
                    "<h4>In the Name of Allah</h4>"
                    "<h5>Brief Biography</h5>"
                    "<p>Born on <strong>14 October 1990</strong> in Gopalpur, District Siwan, Bihar, India — "
                    "in the household of Āyatullāh al-ʿUẓmā Syed Rahat Hussain Hindi Gopalpuri.</p>"
                    "<h5>Educational Journey</h5>"
                    "<ul>"
                    "<li>Madrasah Islamiyah Kajhwa — initial religious education</li>"
                    "<li>Hawzah Ilmiyyah Imam Muhammad Baqir (AS), Bhiwandi — Saraf, Nahw, Mantiq, Usul</li>"
                    "<li>Hawzat al-Mahdi, Hyderabad — Fiqh &amp; advanced Nahw</li>"
                    "<li>Hawzah Ilmiyyah Amir al-Momineen (AS) — Najafi House, Mumbai — Lum'atayn, Usul</li>"
                    "<li>Madrasah Imam Khomeini (ra), Qom — BA in Shia Studies (Karshenasi)</li>"
                    "<li>Madrasah Hujjatiyyah, Qom — MA in Fiqh &amp; Usul (Karshenasi Arshad) — "
                    "studying Kafayat al-Usul under <em>Āyatullāh Syed Nasir al-Din Hussaini</em> "
                    "and Makasib under <em>Āyatullāh Sheikh Muhammad Kazim Elahi</em>. Currently attending "
                    "Dars-e-Kharij of <em>Āyatullāh al-ʿUẓmā Sheikh Muhammad Mahdi Ganji</em>.</li>"
                    "</ul>"
                    "<h5>Scholarly Certifications (Ijāzāt)</h5>"
                    "<p><strong>Ijāzah Naql Riwāyat</strong> from:</p>"
                    "<ul>"
                    "<li>Āyatullāh Ahmad Kalbasi (descendant of Malik al-Ashtar)</li>"
                    "<li>Āyatullāh Syed Kazim Mustafawi (student of Āyatullāh al-ʿUẓmā al-Khoei)</li>"
                    "<li>Āyatullāh al-ʿUẓmā Sheikh Nasir Makarem Shirazi</li>"
                    "<li>Āyatullāh al-ʿUẓmā Sheikh Jafar Subhani</li>"
                    "</ul>"
                    "<p><strong>Ijāzah Wakalat &amp; Sahm-e-Imam</strong> from:</p>"
                    "<ul>"
                    "<li>Āyatullāh Syed Kazim Mustafawi</li>"
                    "<li>Āyatullāh al-ʿUẓmā Sheikh Nasir Makarem Shirazi</li>"
                    "<li>Āyatullāh al-ʿUẓmā Syed Musa Shubayri Zanjani</li>"
                    "<li>Āyatullāh al-ʿUẓmā Syed Ali Hussaini Sistani</li>"
                    "</ul>"
                ),

                # ── Arabic Biography ───────────────────────────────────────
                biography_ar=(
                    "<h4>بسم الله الرحمن الرحيم</h4>"
                    "<h5>نبذة مختصرة عن السيرة الذاتية</h5>"
                    "<p>أحقر الزمن السيد جواد العسكري الرضوي منهال گوپالپوري، ابن المرحوم السيد فخر العباد.</p>"
                    "<p>وُلد الحقير بتاريخ <strong>14 أكتوبر 1990م</strong> في قرية گوپالپور، "
                    "مقاطعة سيوان، بيهار — في دار آية الله العظمى السيد راحت حسين الهندي الگوپالپوري.</p>"
                    "<h5>الرؤية والبداية الدينية</h5>"
                    "<p>في سن العاشرة أو الحادية عشرة تقريباً، كان يرى نفسه في المنام باستمرار "
                    "يرتدي رداء الروحانية ويطير، مما أثار في نفسه الرغبة في طلب العلم الديني.</p>"
                    "<h5>المسيرة التعليمية</h5>"
                    "<ul>"
                    "<li>مدرسة إسلامية كجهوه — التعليم الديني الأولي</li>"
                    "<li>الحوزة العلمية الإمام محمد باقر (ع)، بهيوندي — الصرف والنحو والمنطق وأصول الفقه</li>"
                    "<li>حوزة المهدي، حيدر آباد — الفقه والنحو المتقدم</li>"
                    "<li>الحوزة العلمية أمير المؤمنين (ع) — نجفي هاوس، مومباي — اللمعتان والأصول</li>"
                    "<li>مدرسة الإمام الخميني (ره)، قم — بكالوريوس في الدراسات الشيعية (كارشناسي)</li>"
                    "<li>مدرسة الحجتية، قم — ماجستير في الفقه والأصول (كارشناسي ارشد) — "
                    "يدرس كفاية الأصول تحت إشراف <em>آية الله السيد ناصر الدين الحسيني</em> "
                    "والمكاسب تحت إشراف <em>آية الله الشيخ محمد كاظم إلهي</em>. "
                    "ويحضر حالياً درس الخارج لـ<em>آية الله العظمى الشيخ محمد مهدي كنجي</em>.</li>"
                    "</ul>"
                    "<h5>الإجازات العلمية</h5>"
                    "<p><strong>إجازات نقل الرواية</strong> من:</p>"
                    "<ul>"
                    "<li>آية الله أحمد الكلباسي (من ذرية مالك الأشتر)</li>"
                    "<li>آية الله السيد كاظم المصطفوي (تلميذ آية الله العظمى السيد الخوئي)</li>"
                    "<li>آية الله العظمى الشيخ ناصر مكارم الشيرازي</li>"
                    "<li>آية الله العظمى الشيخ جعفر السبحاني</li>"
                    "</ul>"
                    "<p><strong>إجازات الوكالة وسهم الإمام</strong> من:</p>"
                    "<ul>"
                    "<li>آية الله السيد كاظم المصطفوي</li>"
                    "<li>آية الله العظمى الشيخ ناصر مكارم الشيرازي</li>"
                    "<li>آية الله العظمى السيد موسى شبيري الزنجاني</li>"
                    "<li>آية الله العظمى السيد علي الحسيني السيستاني</li>"
                    "</ul>"
                    "<p><em>وما علينا إلا البلاغ — والسلام عليكم</em></p>"
                    "<p><strong>أحقر العباد السيد منهال حسين گوپالپوري</strong><br>"
                    "١١ فبراير ٢٠٢٦م — ٢٢ شعبان ١٤٤٧هـ</p>"
                ),

                # ── Farsi Biography ────────────────────────────────────────
                biography_fa=(
                    "<h4>بسم الله الرحمن الرحیم</h4>"
                    "<h5>شرح حال مختصر</h5>"
                    "<p>احقر الزمن السید جواد العسکری الرضوی منهال گوپال‌پوری، فرزند مرحوم سید فخر العباد.</p>"
                    "<p>حقیر در تاریخ <strong>۱۴ اکتبر ۱۹۹۰م</strong> در روستای گوپال‌پور، "
                    "شهرستان سیوان، بیهار — در خانه آیت‌الله العظمی سید راحت حسین هندی گوپال‌پوری متولد شد.</p>"
                    "<h5>رؤیا و آغاز تحصیل دینی</h5>"
                    "<p>در سن تقریبی ده یا یازده سالگی، پیوسته در خواب می‌دید که لباس روحانیت پوشیده "
                    "و پرواز می‌کند، که این رؤیا انگیزه روی آوردن به علوم دینی را در او برانگیخت.</p>"
                    "<h5>مسیر تحصیلی</h5>"
                    "<ul>"
                    "<li>مدرسه اسلامیه کجهوه — تحصیلات دینی ابتدایی</li>"
                    "<li>حوزه علمیه امام محمد باقر (ع)، بهیوندی — صرف، نحو، منطق، اصول فقه</li>"
                    "<li>حوزه المهدی، حیدرآباد — فقه و نحو پیشرفته</li>"
                    "<li>حوزه علمیه امیرالمؤمنین (ع) — نجفی هاوس، ممبئی — لمعتان و اصول</li>"
                    "<li>مدرسه امام خمینی (ره)، قم — کارشناسی در شیعه‌شناسی</li>"
                    "<li>مدرسه حجتیه، قم — کارشناسی ارشد فقه و اصول — "
                    "درس کفایةالاصول نزد <em>آیت‌الله سید ناصرالدین حسینی</em> "
                    "و مکاسب نزد <em>آیت‌الله شیخ محمد کاظم الهی</em>. "
                    "در حال حاضر در درس خارج <em>آیت‌الله العظمی شیخ محمد مهدی گنجی</em> شرکت دارد.</li>"
                    "</ul>"
                    "<h5>اجازه‌های علمی</h5>"
                    "<p><strong>اجازه نقل روایت</strong> از:</p>"
                    "<ul>"
                    "<li>آیت‌الله احمد کلباسی (از نسل مالک اشتر)</li>"
                    "<li>آیت‌الله سید کاظم مصطفوی (شاگرد آیت‌الله العظمی سید خویی)</li>"
                    "<li>آیت‌الله العظمی شیخ ناصر مکارم شیرازی</li>"
                    "<li>آیت‌الله العظمی شیخ جعفر سبحانی</li>"
                    "</ul>"
                    "<p><strong>اجازه وکالت و سهم امام</strong> از:</p>"
                    "<ul>"
                    "<li>آیت‌الله سید کاظم مصطفوی</li>"
                    "<li>آیت‌الله العظمی شیخ ناصر مکارم شیرازی</li>"
                    "<li>آیت‌الله العظمی سید موسی شبیری زنجانی</li>"
                    "<li>آیت‌الله العظمی سید علی حسینی سیستانی</li>"
                    "</ul>"
                    "<p><em>و ما علینا الا البلاغ — والسلام علیکم</em></p>"
                    "<p><strong>احقر العباد سید منهال حسین گوپال‌پوری</strong><br>"
                    "۱۱ فوریه ۲۰۲۶م — ۲۲ شعبان ۱۴۴۷ه‍</p>"
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
            # ── Board of Trustees ──────────────────────────────────────────
            dict(name="Syed Minhal Hussain Rizvi (Gopal Puri)", designation="Principal & Founder — Centre of Faqāhat",         phone="+91 8828073319", sort_order=1, member_type="trustee",    photo_file="minhal.jpg"),
            dict(name="Maulana Syed Javed Akhtar Rizvi",        designation="Vice Principal — Imam Juma wa Jama'at, Gopalpur", phone="+91 9973559812", sort_order=2, member_type="trustee",    photo_file="javed_akhtar.jpg"),
            dict(name="Mohammad Feroz Hashemi",                 designation="Treasurer & Trustee — Muhammadiyah Trust",        phone="+91 9702289112", sort_order=3, member_type="trustee",    photo_file="mohammad_feroz_hashemi.jpg"),
            dict(name="Dr. Syed Mohammad Zahid",                designation="Trustee — Muhammadiyah Trust",                    phone="",              sort_order=4, member_type="trustee",    photo_file="syed_md_zahid.jpg"),
            dict(name="Syed Ali Abbas",                         designation="Trustee — Muhammadiyah Trust",                    phone="",              sort_order=5, member_type="trustee",    photo_file="syed_ali_abbas.jpg"),
            dict(name="Syed Mohammad Ibrahim",                  designation="Trustee — Muhammadiyah Trust",                    phone="",              sort_order=6, member_type="trustee",    photo_file="ibrahim_chacha.jpg"),
            dict(name="Syed Mohammad Abbas",                    designation="Trustee — Muhammadiyah Trust",                    phone="",              sort_order=7, member_type="trustee",    photo_file="md_abbas.jpeg"),
            # ── Consulting Members ─────────────────────────────────────────
            dict(name="Hujjatul Islam wal Muslemeen Syed Abul Qasim", designation="President of Shia Ulema Council (Australia)", phone="", sort_order=8, member_type="consultant", photo_file="syed_abulqasim.jpg"),
            dict(name="Dr. Syed Mohammad Rizvi",                designation="",                                                 phone="",              sort_order=9, member_type="consultant", photo_file="syed_md_rizvi.jpg"),
            dict(name="Syed Ehtesham Hussain",                  designation="",                                                 phone="",              sort_order=10, member_type="consultant", photo_file="syed_ehtesham.jpg"),
        ]
        media_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "media", "team")
        for t in trustees:
            photo_file = t.pop("photo_file")
            obj, created = Trustee.objects.get_or_create(name=t["name"], defaults={**t, "is_active": True})
            # Always sync member_type, sort_order and designation on existing records
            if not created:
                changed = False
                for field in ("member_type", "sort_order", "designation"):
                    if getattr(obj, field) != t.get(field, getattr(obj, field)):
                        setattr(obj, field, t[field])
                        changed = True
                if changed:
                    obj.save(update_fields=["member_type", "sort_order", "designation"])
            # Attach photo only if not already set
            if photo_file and (not obj.photo):
                photo_path = os.path.join(media_dir, photo_file)
                if os.path.exists(photo_path):
                    with open(photo_path, "rb") as f:
                        obj.photo.save(photo_file, File(f), save=True)
            self._log(f"Trustee ({t['member_type']}): {t['name']}", created)

    # ── Ijazah ─────────────────────────────────────────────────────────────
    def _seed_ijazah(self):
        from django.core.files import File
        import os
        from core.models import Ijazah

        media_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "media", "ijazah")
        ijazah = [
            dict(title="Ijāzah Naql Riwāyat — Āyatullāh Ahmad Kalbasi",          from_scholar="Āyatullāh Ahmad Kalbasi",                ijazah_type="riwayat",   sort_order=1, photo_file="riwayat_kalbasi.jpg"),
            dict(title="Ijāzah Naql Riwāyat — Āyatullāh Syed Kazim Mustafawi",   from_scholar="Āyatullāh Syed Kazim Mustafawi",         ijazah_type="riwayat",   sort_order=2, photo_file="riwayat_mustafawi.jpg"),
            dict(title="Ijāzah Naql Riwāyat — Āyatullāh Nasir Makarem Shirazi",  from_scholar="Āyatullāh Nasir Makarem Shirazi",        ijazah_type="riwayat",   sort_order=3, photo_file="riwayat_makarem.jpg"),
            dict(title="Ijāzah Naql Riwāyat — Āyatullāh Jafar Subhani (p.1)",   from_scholar="Āyatullāh Sheikh Jafar Subhani",         ijazah_type="riwayat",   sort_order=4, photo_file="riwayat_subhani_p1.jpg"),
            dict(title="Ijāzah Naql Riwāyat — Āyatullāh Jafar Subhani (p.2)",   from_scholar="Āyatullāh Sheikh Jafar Subhani",         ijazah_type="riwayat",   sort_order=5, photo_file="riwayat_subhani_p2.jpg"),
            dict(title="Ijāzah Wakalat — Āyatullāh Syed Kazim Mustafawi",        from_scholar="Āyatullāh Syed Kazim Mustafawi",         ijazah_type="wakalat",   sort_order=6, photo_file="wakalat_mustafawi.jpg"),
            dict(title="Ijāzah Wakalat — Āyatullāh Nasir Makarem Shirazi",       from_scholar="Āyatullāh Nasir Makarem Shirazi",        ijazah_type="wakalat",   sort_order=7, photo_file="wakalat_makarem.jpg"),
            dict(title="Ijāzah Wakalat — Āyatullāh Syed Musa Shubayri Zanjani", from_scholar="Āyatullāh Syed Musa Shubayri Zanjani",   ijazah_type="wakalat",   sort_order=8, photo_file="wakalat_zanjani.jpg"),
            dict(title="Ijāzah Sahm-e-Imam — Āyatullāh Syed Ali Sistani",       from_scholar="Āyatullāh Syed Ali Hussaini Sistani",    ijazah_type="sahm_imam", sort_order=9, photo_file="sahm_sistani.jpg"),
        ]
        for ij in ijazah:
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
            dict(
                subject="quran",
                title_en="Qurʾān", title_ar="القرآن الكريم", title_ur="قرآن کریم", title_fa="قرآن کریم",
                icon_class="fas fa-book-open", sort_order=1,
                description_en="<p>Study of the Holy Qurʾān including recitation (Tajweed), memorisation (Hifz), and principles of interpretation (Tafsir).</p>",
                description_ar="<p>دراسة القرآن الكريم بما تشمل التجويد والحفظ وأصول التفسير.</p>",
                description_ur="<p>قرآن کریم کا مطالعہ جس میں تجوید، حفظ اور اصول تفسیر شامل ہیں۔</p>",
                description_fa="<p>مطالعه قرآن کریم شامل تجوید، حفظ و اصول تفسیر.</p>",
            ),
            dict(
                subject="hadith",
                title_en="Hadith", title_ar="علم الحديث", title_ur="علم حدیث", title_fa="علم حدیث",
                icon_class="fas fa-scroll", sort_order=2,
                description_en="<p>Study of the transmitted sayings and actions of the Prophet ﷺ and the Imams (AS), including the science of narrators (Rijal).</p>",
                description_ar="<p>دراسة الأحاديث المنقولة عن النبي ﷺ والأئمة (ع)، وتشمل علم الرجال.</p>",
                description_ur="<p>پیغمبر ﷺ اور ائمہ (ع) کے منقول اقوال و افعال کا مطالعہ، جس میں علم رجال بھی شامل ہے۔</p>",
                description_fa="<p>مطالعه احادیث منقول از پیامبر ﷺ و ائمه (ع) شامل علم رجال.</p>",
            ),
            dict(
                subject="Fiqh",
                title_en="Fiqh", title_ar="الفقه", title_ur="فقہ", title_fa="فقه",
                icon_class="fas fa-balance-scale", sort_order=3,
                description_en="<p>Islamic jurisprudence — the practical legal rulings derived from the Qurʾān and Sunnah covering worship, transactions, and personal conduct.</p>",
                description_ar="<p>الفقه الإسلامي — الأحكام الشرعية المستنبطة من القرآن والسنة في العبادات والمعاملات والأحوال الشخصية.</p>",
                description_ur="<p>اسلامی فقہ — قرآن و سنت سے مستنبط عملی شرعی احکام، جن میں عبادات، معاملات اور اخلاقیات شامل ہیں۔</p>",
                description_fa="<p>فقه اسلامی — احکام شرعی عملی مستنبط از قرآن و سنت در عبادات، معاملات و رفتار فردی.</p>",
            ),
            dict(
                subject="usul",
                title_en="Usūl al-Fiqh", title_ar="أصول الفقه", title_ur="اصول الفقہ", title_fa="اصول فقه",
                icon_class="fas fa-sitemap", sort_order=4,
                description_en="<p>The principles and methodology used to derive Islamic legal rulings — the foundational science underpinning all jurisprudence.</p>",
                description_ar="<p>المبادئ والمنهجية المستخدمة لاستنباط الأحكام الشرعية — العلم الأساسي الذي يقوم عليه الفقه كله.</p>",
                description_ur="<p>شرعی احکام کے استنباط میں استعمال ہونے والے اصول و طریقہ کار — فقہ کی بنیادی سائنس۔</p>",
                description_fa="<p>اصول و روش‌شناسی استنباط احکام شرعی — علم پایه‌ای که زیربنای همه فقه است.</p>",
            ),
            dict(
                subject="kalam",
                title_en="Kalām & ʿAqīdah", title_ar="الكلام والعقيدة", title_ur="کلام و عقیدہ", title_fa="کلام و عقیده",
                icon_class="fas fa-star-and-crescent", sort_order=5,
                description_en="<p>Islamic theology and creed — rational study of the fundamentals of faith including theology, philosophy, and apologetics.</p>",
                description_ar="<p>علم الكلام والعقيدة الإسلامية — الدراسة العقلية لأصول الدين بما يشمل اللاهوت والفلسفة وعلم الجدل.</p>",
                description_ur="<p>اسلامی علم کلام اور عقیدہ — ایمان کے بنیادی اصولوں کا عقلی مطالعہ جس میں الہیات، فلسفہ اور دفاع دین شامل ہے۔</p>",
                description_fa="<p>کلام و عقیده اسلامی — مطالعه عقلانی مبانی دین شامل الهیات، فلسفه و دفاع از دین.</p>",
            ),
            dict(
                subject="akhlaq",
                title_en="Akhlāq", title_ar="الأخلاق", title_ur="اخلاق", title_fa="اخلاق",
                icon_class="fas fa-heart", sort_order=6,
                description_en="<p>Islamic ethics and spiritual refinement — study of virtuous character, self-purification, and the moral teachings of the Quran and Ahlul Bayt (AS).</p>",
                description_ar="<p>الأخلاق الإسلامية والتزكية الروحية — دراسة الفضائل وتهذيب النفس والتعاليم الأخلاقية للقرآن وأهل البيت (ع).</p>",
                description_ur="<p>اسلامی اخلاق اور روحانی تزکیہ — فضائل، تزکیۂ نفس اور قرآن و اہل بیت (ع) کی اخلاقی تعلیمات کا مطالعہ۔</p>",
                description_fa="<p>اخلاق اسلامی و تزکیه روحانی — مطالعه فضایل، تهذیب نفس و تعالیم اخلاقی قرآن و اهل بیت (ع).</p>",
            ),
            dict(
                subject="rational",
                title_en="Rational Sciences", title_ar="العلوم العقلية", title_ur="عقلی علوم", title_fa="علوم عقلی",
                icon_class="fas fa-brain", sort_order=7,
                description_en="<p>Logic (Mantiq), Philosophy (Falsafa), and related rational disciplines that form the intellectual backbone of advanced Islamic scholarship.</p>",
                description_ar="<p>المنطق والفلسفة والعلوم العقلية المرتبطة التي تشكّل العمود الفقري الفكري للاجتهاد الإسلامي المتقدم.</p>",
                description_ur="<p>منطق، فلسفہ اور متعلقہ عقلی علوم جو اعلیٰ اسلامی علمی تحقیق کی فکری ریڑھ کی ہڈی ہیں۔</p>",
                description_fa="<p>منطق، فلسفه و علوم عقلی مرتبط که ستون فقرات فکری اجتهاد پیشرفته اسلامی را تشکیل می‌دهند.</p>",
            ),
            dict(
                subject="language",
                title_en="Language & Literature", title_ar="اللغة والأدب", title_ur="زبان و ادب", title_fa="زبان و ادبیات",
                icon_class="fas fa-language", sort_order=8,
                description_en="<p>Advanced Arabic grammar (Nahw, Sarf), rhetoric (Balaghah), and Persian and English language proficiency for scholarly research and communication.</p>",
                description_ar="<p>النحو والصرف والبلاغة العربية المتقدمة، مع إتقان اللغتين الفارسية والإنجليزية للبحث العلمي والتواصل.</p>",
                description_ur="<p>عربی نحو، صرف اور بلاغت کے اعلیٰ اسباق، نیز علمی تحقیق اور ابلاغ کے لیے فارسی اور انگریزی زبان میں مہارت۔</p>",
                description_fa="<p>نحو، صرف و بلاغت پیشرفته عربی، به همراه تسلط بر زبان‌های فارسی و انگلیسی برای پژوهش علمی و ارتباط.</p>",
            ),
        ]
        for p in programs:
            obj, created = AcademicProgram.objects.update_or_create(
                subject=p["subject"],
                defaults={**p, "is_active": True}
            )
            self._log(f"AcademicProgram: {p['title_en']}", created)

    # ── Subjects (for Lessons) ─────────────────────────────────────────────
    def _seed_subjects(self):
        subjects = [
            dict(slug="tafsir",   title_en="Tafsir",               title_ar="التفسير",          title_ur="تفسیر",         title_fa="تفسیر",          icon_class="fas fa-book-open",         sort_order=1),
            dict(slug="hadith",   title_en="Hadith",               title_ar="علم الحديث",       title_ur="علم حدیث",      title_fa="علم حدیث",        icon_class="fas fa-scroll",            sort_order=2),
            dict(slug="Fiqh",     title_en="Fiqh",                 title_ar="الفقه",            title_ur="فقہ",           title_fa="فقه",             icon_class="fas fa-balance-scale",     sort_order=3),
            dict(slug="usul",     title_en="Usūl al-Fiqh",         title_ar="أصول الفقه",       title_ur="اصول الفقہ",    title_fa="اصول فقه",        icon_class="fas fa-sitemap",           sort_order=4),
            dict(slug="kalam",    title_en="Kalām & ʿAqīdah",     title_ar="الكلام والعقيدة",  title_ur="کلام و عقیدہ",  title_fa="کلام و عقیده",    icon_class="fas fa-star-and-crescent", sort_order=5),
            dict(slug="akhlaq",   title_en="Akhlāq",               title_ar="الأخلاق",          title_ur="اخلاق",         title_fa="اخلاق",           icon_class="fas fa-heart",             sort_order=6),
            dict(slug="rational", title_en="Rational Sciences",    title_ar="العلوم العقلية",   title_ur="عقلی علوم",     title_fa="علوم عقلی",       icon_class="fas fa-brain",             sort_order=7),
            dict(slug="arabic",   title_en="Arabic Literature",    title_ar="الأدب العربي",     title_ur="عربی ادب",      title_fa="ادبیات عربی",     icon_class="fas fa-language",          sort_order=8),
        ]
        for s in subjects:
            obj, created = Subject.objects.update_or_create(slug=s["slug"], defaults={**s, "is_active": True})
            self._log(f"Subject: {s['title_en']}", created)

    # ── Announcement Categories ────────────────────────────────────────────
    # AnnouncementCategory uses 'slug' with SLUG_CHOICES: statement, message, event
    def _seed_announcement_categories(self):
        cats = [
            dict(slug="statement", title_en="Statement",      title_ar="البيانات",            title_ur="بیانیہ",         title_fa="بیانیه"),
            dict(slug="message",   title_en="Issued Message", title_ar="الرسائل الصادرة",      title_ur="جاری کردہ پیغام", title_fa="پیام صادره"),
            dict(slug="event",     title_en="Events",         title_ar="الفعاليات والمناسبات", title_ur="تقریبات",         title_fa="رویدادها"),
        ]
        for c in cats:
            obj, created = AnnouncementCategory.objects.get_or_create(
                slug=c["slug"],
                defaults={
                    "title_en": c["title_en"],
                    "title_ar": c["title_ar"],
                    "title_ur": c.get("title_ur", ""),
                    "title_fa": c.get("title_fa", ""),
                }
            )
            self._log(f"AnnouncementCategory: {c['title_en']}", created)

    # ── Book Categories ────────────────────────────────────────────────────
    # BookCategory uses CATEGORY_CHOICES slugs: tafsir_hadith, rijal, Fiqh, usul, kalam, akhlaq, rational, arabic, misc
    def _seed_book_categories(self):
        cats = [
            dict(slug="tafsir_hadith", title_en="Tafsīr & Hadith",    sort_order=1),
            dict(slug="rijal",         title_en="Rijāl",               sort_order=2),
            dict(slug="Fiqh",          title_en="Fiqh",                sort_order=3),
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
    # ShariaCategory uses 'name' field with CATEGORY_CHOICES: kalam, akhlaq, Fiqh
    def _seed_sharia_categories(self):
        cats = [
            dict(name="kalam",  title_en="Kalām & ʿAqīdah", title_ar="الكلام والعقيدة"),
            dict(name="akhlaq", title_en="Akhlāq",           title_ar="الأخلاق"),
            dict(name="Fiqh",   title_en="Fiqh",             title_ar="الفقه"),
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
