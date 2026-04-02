# مدرسة مدينة العلم — Madrasah Madinatul Ilm
## Centre of Faqāhat | Under Muhammadiyah Trust

**Established:** 14 Sha'ban 1447 AH / 3 February 2026  
**Location:** Gopalpur, Siwan, Bihar, India — 841286  
**Founder:** Syed Minhal Hussain Rizvi  

---

## 🏗 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.2 |
| REST API | Django REST Framework |
| Database | SQLite (dev) → MySQL (production) |
| Rich Text | django-ckeditor |
| Frontend | Bootstrap 5 + custom CSS/JS |
| Fonts | Amiri (Arabic), Playfair Display, Lato |
| Animations | AOS |

---

## 📁 Project Structure

```
madinatulilm/
├── madinatulilm/        # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                # Homepage, About, Founder, Trustees, Academics
├── quran_app/           # Quran resources
├── sharia/              # Kalam, Akhlaq, Fiqh content
├── announcements/       # Statements, Messages, Meetings
├── lessons/             # Structured lessons by subject
├── books/               # Books & Articles library
├── contact/             # Contact form & Q&A
├── templates/           # HTML templates
├── static/              # CSS, JS, images
│   ├── css/main.css
│   └── js/main.js
├── media/               # Uploaded files (runtime)
├── content/             # Drop your source files here
│   ├── 01_home/
│   ├── 02_quran/
│   ├── 03_sharia/
│   ├── 04_announcements/
│   ├── 05_lessons/
│   ├── 06_books/
│   ├── 07_about/
│   ├── 08_contact/
│   └── 09_academics/
└── MohammadiyahTrust/   # Original source documents
```

---

## 🚀 Quick Start (Development)

```bash
# 1. Activate venv
source /Users/sazmham/Documents/personal_projects/venv/bin/activate

# 2. Install deps
pip install -r requirements.txt

# 3. Run migrations
cd madinatulilm
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Load initial data (optional)
python manage.py loaddata initial_data.json

# 6. Start server
python manage.py runserver
```

Open: http://127.0.0.1:8000  
Admin: http://127.0.0.1:8000/admin

---

## 🗄 MySQL (Production)

Edit `.env`:
```
DB_ENGINE=django.db.backends.mysql
DB_NAME=madinatulilm
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

Create the database:
```sql
CREATE DATABASE madinatulilm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 🌐 REST API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/settings/` | Site settings |
| `GET /api/v1/founder/` | Founder info |
| `GET /api/v1/programs/` | Academic programs |
| `GET /api/v1/quran/` | Quran resources |
| `GET /api/v1/sharia/` | Sharia content |
| `GET /api/v1/announcements/` | Announcements |
| `GET /api/v1/lessons/` | Lessons |
| `GET /api/v1/books/` | Books & Articles |
| `POST /api/v1/contact/` | Submit contact message |
| `POST /api/v1/contact/ask/` | Submit question |
| `GET /api/v1/contact/public-qa/` | Public Q&A |

---

## 📦 Website Menu (as per Menu for website.docx)

1. **Introduction** — Home, About, Founder, Academics
2. **Quran** — Resources, Texts, Audio
3. **Sharia Matters** — Kalam, Akhlaq, Fiqh
4. **Announcements** — Statement, Issued Message, Meeting
5. **Lessons** — Tafsir, Hadith, Fiqh, Usul, Kalam, Akhlaq, Rational Sciences, Arabic
6. **Books & Articles** — 9 categories
7. **Ask a Question** — Public Q&A form
8. **Contact Us** — Message form + info

---

## 📞 Contact

**Principal & Founder:** Syed Minhal Hussain Rizvi  
+91 8828073319 | +98 9055171993  

**Vice Principal:** Maulana Syed Javed Akhtar  
+91 9973559812  

**Address:** Madrasa Madinatul Ilm, Gopal Pur, Post: Baqir Ganj,  
Thana: Hussain Ganj, District: Siwan, Bihar — 841286
