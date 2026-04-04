"""
Management command: python manage.py seed_hadiths
Seeds HadithQuote and PartnerPage. Safe to re-run — hadiths are fully replaced.
First hadith is always the famous "Ana Madinatul Ilm" hadith — the namesake of the madrasah.
All hadiths have content in all 4 site languages (EN, AR, UR, FA).
"""
from django.core.management.base import BaseCommand
from core.models import HadithQuote, PartnerPage


HADITHS = [
    {
        # ── The namesake hadith — always first (sort_order=0) ──────────────
        # text_ar: pure hadith body only — no "qala..." prefix
        "text_ar":  "أَنَا مَدِينَةُ الْعِلْمِ وَعَلِيٌّ بَابُهَا، "
                    "فَمَنْ أَرَادَ الْمَدِينَةَ فَلْيَأْتِ الْبَابَ",
        "text_en":  "I am the city of knowledge and ʿAlī is its gate — "
                    "whoever wishes to enter the city must come through the gate.",
        "text_ur":  "میں علم کا شہر ہوں اور علی اس کا دروازہ ہیں — "
                    "جو بھی اس شہر میں آنا چاہے وہ دروازے سے آئے۔",
        "text_fa":  "من شهر علمم و علی دروازه آن است — "
                    "هر کس خواهد وارد شهر شود باید از دروازه بیاید.",
        "source":   "Al-Mustadrak ʿalā al-Ṣaḥīḥayn, Vol. 3 p. 126 | "
                    "Biḥār al-Anwār, Vol. 40 p. 201",
        "narrator": "Prophet Muḥammad (S)",
        "sort_order": 0,
    },
    {
        "text_ar":  "الْعِلْمُ أَصْلُ كُلِّ خَيْرٍ",
        "text_en":  "Knowledge is the root of every good.",
        "text_ur":  "علم ہر بھلائی کی جڑ ہے۔",
        "text_fa":  "علم ریشه هر خیری است.",
        "source":   "Ghurar al-Ḥikam, No. 1611",
        "narrator": "Imam ʿAlī ibn Abī Ṭālib (AS)",
        "sort_order": 1,
    },
    {
        "text_ar":  "طَلَبُ الْعِلْمِ فَرِيضَةٌ عَلَى كُلِّ مُسْلِمٍ",
        "text_en":  "Seeking knowledge is an obligation upon every Muslim.",
        "text_ur":  "علم حاصل کرنا ہر مسلمان پر فرض ہے۔",
        "text_fa":  "طلب علم بر هر مسلمانی واجب است.",
        "source":   "Biḥār al-Anwār, Vol. 1 p. 177",
        "narrator": "Prophet Muḥammad (S)",
        "sort_order": 2,
    },
    {
        "text_ar":  "اعْرِفْ مَنَازِلَ الشِّيعَةِ عَلَى قَدْرِ رِوَايَتِهِمْ وَعِلْمِهِمْ",
        "text_en":  "Recognise the station of the Shīʿa by the degree of their narration and knowledge.",
        "text_ur":  "شیعوں کے مراتب کو ان کی روایت اور علم کی مقدار سے پہچانو۔",
        "text_fa":  "منزلت شیعیان را به اندازه روایت و دانش آنان بشناسید.",
        "source":   "Al-Kāfī, Vol. 1 p. 50",
        "narrator": "Imam Jaʿfar al-Ṣādiq (AS)",
        "sort_order": 3,
    },
    {
        "text_ar":  "قِيمَةُ كُلِّ امْرِئٍ مَا يُحْسِنُهُ",
        "text_en":  "The value of every person lies in what they master.",
        "text_ur":  "ہر انسان کی قدر و قیمت وہی ہے جو وہ اچھی طرح جانتا ہے۔",
        "text_fa":  "ارزش هر کس به چیزی است که بدان تسلط دارد.",
        "source":   "Nahj al-Balāgha, Ḥikma 81",
        "narrator": "Imam ʿAlī ibn Abī Ṭālib (AS)",
        "sort_order": 4,
    },
    {
        "text_ar":  "تَذَاكَرُ الْعِلْمِ دِرَاسَةٌ وَالدِّرَاسَةُ صَلَاةٌ حَسَنَةٌ",
        "text_en":  "Discussing knowledge is study, and study is a virtuous act of worship.",
        "text_ur":  "علم کا تذکرہ مطالعہ ہے اور مطالعہ بہترین عبادت ہے۔",
        "text_fa":  "مذاکره علم درس است و درس نمازی نیکو است.",
        "source":   "Al-Kāfī, Vol. 1 p. 41",
        "narrator": "Imam Muḥammad al-Bāqir (AS)",
        "sort_order": 5,
    },
    {
        "text_ar":  "لَا كَنْزَ أَنْفَعُ مِنَ الْعِلْمِ",
        "text_en":  "There is no treasure more beneficial than knowledge.",
        "text_ur":  "علم سے زیادہ نفع بخش کوئی خزانہ نہیں۔",
        "text_fa":  "هیچ گنجی سودمندتر از علم نیست.",
        "source":   "Ghurar al-Ḥikam, No. 10704",
        "narrator": "Imam ʿAlī ibn Abī Ṭālib (AS)",
        "sort_order": 6,
    },
]

BANK_DETAILS = """Beneficiary: Muhammadiyyah Educational & Social Welfare Trust
Name of Bank: ICICI Bank
Branch: Siwan, Bihar
Account No.: 000000000
IFSC: 000000000

Beneficiary: Muhammadiyyah Educational & Social Welfare Trust
Name of Bank: State Bank of India
Branch: Gopal Pur, Bihar
Account No.: 000000000
IFSC: 000000000"""


class Command(BaseCommand):
    help = "Seed HadithQuote and PartnerPage initial data"

    def handle(self, *args, **options):
        # Always replace hadith data so sort_order/content stays consistent
        HadithQuote.objects.all().delete()
        for h in HADITHS:
            HadithQuote.objects.create(**h)
        self.stdout.write(self.style.SUCCESS(
            f"  Hadiths: {len(HADITHS)} seeded "
            "(first = 'Anā Madīnatul ʿIlm…')"
        ))

        pp, made = PartnerPage.objects.get_or_create(
            id=1,
            defaults={
                "bank_details": BANK_DETAILS,
                "tax_note":     "Tax Benefit: Applied For",
                "is_active":    True,
            }
        )
        self.stdout.write(self.style.SUCCESS(
            f"  PartnerPage: {'created' if made else 'already exists'}"
        ))
        self.stdout.write(self.style.SUCCESS("  seed_hadiths complete ✓"))
