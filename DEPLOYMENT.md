# Madrasah Madinatul Ilm — Deployment Guide

---

## 1. Accessing the Admin Panel (Local Dev)

The server is already running locally. Open:

```
http://127.0.0.1:8000/admin/
```

| Field    | Value             |
|----------|-------------------|
| Username | `admin`           |
| Password | `MIL@admin2026!`  |

> **Change this password immediately** after first login in production.
> Admin → Users → admin → Set password

---

## 2. What You Can Manage in the Admin Panel

| Section | What You Can Do |
|---------|----------------|
| **Core** | Site Settings, Welcome / Mission / Vision / About text, Founder bio, Trustees, Ijazah certificates, Gallery photos, Academic Programs |
| **Announcements** | Create / edit announcements and categories |
| **Lessons** | Add lesson series, individual lessons (video/audio/PDF), subjects |
| **Books** | Upload books with PDFs, covers, categories |
| **Sharia** | Add Sharia questions/answers by category |
| **Quran App** | Add Quran recitation pages / notes |
| **Contact** | View submitted contact messages and Q&A submissions |

---

## 3. Updating an Existing Deployment (PythonAnywhere)

> Use this when the site is already live and you want to push new code changes.
> **Do NOT re-run `deploy_pythonanywhere.sh`** — that script is for fresh installs only.

Open a **PythonAnywhere Bash console** and run:

```bash
# 1. Activate virtualenv
source ~/venv_madinatulilm/bin/activate

# 2. Back up .env and media folder first
cp ~/madinatulilm/.env ~/env_backup
cp -r ~/madinatulilm/media ~/media_backup

# 3. Remove old code and re-clone latest
cd ~
rm -rf madinatulilm
git clone https://github.com/mahashemi/madinatulilm.git
cd madinatulilm

# 4. Restore .env and media
cp ~/env_backup .env
cp -r ~/media_backup/* media/

# 5. Install/update dependencies
pip install -r requirements.txt

# 6. Apply any new migrations
python manage.py migrate --noinput

# 7. Collect static files (picks up CSS/JS/template changes)
python manage.py collectstatic --noinput

# 8. Reload the web app
touch /var/www/madrasahmadinatu_pythonanywhere_com_wsgi.py
```

---

## 4. Full Fresh Deployment (New Server)

### Step 1 — Prerequisites on the server (Ubuntu/Debian)

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv \
    nginx git mysql-server libmysqlclient-dev pkg-config
```

### Step 2 — Clone the project

```bash
cd /var/www
git clone <your-git-repo-url> madinatulilm
cd madinatulilm
```

Or copy files via SCP:
```bash
scp -r /Users/sazmham/Documents/personal_projects/madinatulilm/ user@your-server:/var/www/madinatulilm/
```

### Step 3 — Create virtual environment & install dependencies

```bash
cd /var/www/madinatulilm
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn mysqlclient
```

### Step 4 — Set up MySQL database

```sql
-- Run in MySQL shell: mysql -u root -p
CREATE DATABASE madinatulilm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'miluser'@'localhost' IDENTIFIED BY 'StrongPassword123!';
GRANT ALL PRIVILEGES ON madinatulilm.* TO 'miluser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 5 — Configure production .env

Edit `/var/www/madinatulilm/.env`:

```env
DEBUG=False
SECRET_KEY=<generate-a-new-50-char-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=madinatulilm
DB_USER=miluser
DB_PASSWORD=StrongPassword123!
DB_HOST=localhost
DB_PORT=3306
```

Generate a secret key:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 6 — Run migrations, collect static, seed, create admin

```bash
cd /var/www/madinatulilm
source venv/bin/activate

# Run all migrations
python manage.py migrate

# Collect static files to /var/www/madinatulilm/staticfiles/
python manage.py collectstatic --noinput

# Seed all initial content (trustees, ijazah, programs, categories, etc.)
python manage.py seed_content

# Create admin superuser
python manage.py create_superuser
# Or with custom credentials:
DJANGO_SUPERUSER_USERNAME=minhal \
DJANGO_SUPERUSER_EMAIL=admin@madinatulilm.com \
DJANGO_SUPERUSER_PASSWORD='YourNewPassword!' \
python manage.py create_superuser
```

### Step 7 — Copy media files to server

```bash
# From your local machine:
scp -r /Users/sazmham/Documents/personal_projects/madinatulilm/media/ \
    user@your-server:/var/www/madinatulilm/media/
```

### Step 8 — Set up Gunicorn (WSGI server)

Create `/etc/systemd/system/madinatulilm.service`:

```ini
[Unit]
Description=Madrasah Madinatul Ilm — Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/madinatulilm
EnvironmentFile=/var/www/madinatulilm/.env
ExecStart=/var/www/madinatulilm/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/madinatulilm.sock \
    madinatulilm.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable madinatulilm
sudo systemctl start madinatulilm
sudo systemctl status madinatulilm
```

### Step 9 — Configure Nginx

Create `/etc/nginx/sites-available/madinatulilm`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Static files
    location /static/ {
        alias /var/www/madinatulilm/staticfiles/;
        expires 30d;
    }

    # Media files (uploaded photos, PDFs, etc.)
    location /media/ {
        alias /var/www/madinatulilm/media/;
        expires 7d;
    }

    # Django app via Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/madinatulilm.sock;
    }

    client_max_body_size 50M;
}
```

Enable and reload:
```bash
sudo ln -s /etc/nginx/sites-available/madinatulilm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 10 — SSL with Let's Encrypt (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
sudo certbot renew --dry-run   # test auto-renewal
```

### Step 11 — File permissions

```bash
sudo chown -R www-data:www-data /var/www/madinatulilm/media/
sudo chown -R www-data:www-data /var/www/madinatulilm/staticfiles/
sudo chmod -R 755 /var/www/madinatulilm/
```

---

## 4. Quick-Start Commands Summary

```bash
# ── Local development ────────────────────────────────────
cd /Users/sazmham/Documents/personal_projects/madinatulilm
source ../venv/bin/activate
python manage.py runserver                    # start dev server
open http://127.0.0.1:8000                   # website
open http://127.0.0.1:8000/admin/            # admin panel

# ── One-time setup (already done locally) ───────────────
python manage.py migrate                      # create tables
python manage.py seed_content                 # seed all data
python manage.py create_superuser             # create admin user
python manage.py collectstatic --noinput      # for production only

# ── Production server ────────────────────────────────────
sudo systemctl restart madinatulilm           # restart app
sudo systemctl reload nginx                   # reload web server
sudo journalctl -u madinatulilm -f            # view live logs
```

---

## 5. Updating the Site After Code Changes

```bash
cd /var/www/madinatulilm
source venv/bin/activate
git pull origin main                          # pull latest code
pip install -r requirements.txt               # update packages if needed
python manage.py migrate                      # run any new migrations
python manage.py collectstatic --noinput      # update static files
sudo systemctl restart madinatulilm           # restart Gunicorn
```

---

## 6. Recommended Hosting Providers

| Provider | Notes |
|----------|-------|
| **DigitalOcean Droplet** | $6/mo, easy Django setup, recommended |
| **Hetzner VPS** | Very affordable, EU/India-friendly |
| **Linode (Akamai)** | Reliable, $5/mo basic |
| **AWS EC2 t3.micro** | Free tier 1 year, then ~$8/mo |
| **Railway.app** | Zero-config deploy, good for quick start |
| **PythonAnywhere** | Django-friendly, free tier available |

---

## 7. Admin Panel URL Summary

| Environment | URL |
|------------|-----|
| Local dev | http://127.0.0.1:8000/admin/ |
| Production | https://yourdomain.com/admin/ |

**Default credentials (change in production!):**
- Username: `admin`
- Password: `MIL@admin2026!`

---

## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `502 Bad Gateway` | `sudo systemctl restart madinatulilm` |
| Static files not loading | `python manage.py collectstatic --noinput` + check Nginx `alias` path |
| Media files 404 | Check `MEDIA_ROOT` in settings + Nginx `/media/` alias |
| DB connection error | Check `.env` DB credentials + MySQL user grants |
| `django.db.utils.OperationalError` | Run `python manage.py migrate` |
| Admin page unstyled | Run `collectstatic`, check `STATIC_ROOT` in settings |

---

*Generated for Madrasah Madinatul Ilm — Muhammadiyah Trust, Gopalpur, Siwan, Bihar*

---

## 9. Issues Fixed & How — Runbook

A living log of significant bugs and how they were resolved. Use this as a reference for future maintenance.

---

### 9.1 Trustee / Team Photos Not Showing (April 2026)

**Symptom:** Photos uploaded via the Admin panel were not displayed on the About page (team section). The file existed on disk but the `<img>` src returned 404.

**Root cause (two parts):**

1. **DB path mismatch** — Photos were uploaded to `trustees/` or `media/trustees/` but the `Trustee.photo` field had `upload_to="team/"`. Old rows still held old paths like `trustees/minhal_61FpnKT.jpg` while the `MEDIA_URL` mapping expected `team/`.
2. **Missing nginx `/media/` mapping** — On PythonAnywhere the `/media/` URL was not mapped to the `media/` directory in the Web tab → Static files section.

**Fix applied:**

```bash
# SSH into PythonAnywhere and run in Django shell:
source ~/venv_madinatulilm/bin/activate
cd ~/madinatulilm
python manage.py shell

# Then in the shell:
from core.models import Trustee
mapping = {
    "Minhal":    "team/minhal_61FpnKT.jpg",
    "Javed":     "team/javed_akhtar_2VLSk8h.jpg",
    "Hashemi":   "team/mohammad_feroz_hashemi_zPn7Mxn.jpg",
    "Zahid":     "team/syed_md_zahid_A0qcmxf.jpg",
    "Ali Abbas": "team/syed_ali_abbas_EVA9n0j.jpg",
    "Ibrahim":   "team/ibrahim_chacha_I8qYaT0.jpg",
    "Mohammad Abbas": "team/md_abbas_6xxVX1n.jpeg",
    "Abul Qasim": "team/syed_abulqasim_WX5aq95.jpg",
    "Rizvi":     "team/syed_md_rizvi_woDE0tk.jpg",
    "Ehtesham":  "team/syed_ehtesham_NlMurOC.jpg",
}
for keyword, path in mapping.items():
    t = Trustee.objects.filter(name__icontains=keyword).first()
    if t:
        t.photo = path
        t.save()
        print(f"Fixed: {t.name}")
```

**Then in PythonAnywhere Web tab → Static files — add:**

| URL | Directory |
|-----|-----------|
| `/media/` | `/home/madrasahmadinatulilm/madinatulilm/media/` |

Click **Reload**.

---

### 9.2 Maraji (Spiritual Authority) Banner Not Showing Photo (April 2026)

**Symptom:** The Maraji hero banner on the homepage showed no photo.

**Root cause:** The `Maraji` DB record existed but `photo` was blank (the static file `maraje_rahat_hussain.png` was never linked to the DB record).

**Fix applied:**

```bash
python manage.py shell
from core.models import Maraji
m = Maraji.objects.first()
m.photo = "maraji/maraje_rahat_hussain_AntcsVV.png"
m.save()
```

> The file must exist at `media/maraji/maraje_rahat_hussain_AntcsVV.png` on the server.

---

### 9.3 Be A Partner — Bank Details Not Configurable (April 2026)

**Symptom:** Bank account numbers, IFSC codes, and bank names were hard-coded in `partner.html` with placeholder `000000000` values.

**Fix applied:**

- Added structured fields to `PartnerPage` model (`bank1_name`, `bank1_account_no`, `bank1_ifsc`, `bank2_name`, `bank2_account_no`, `bank2_ifsc`, etc.)
- Created migration `0010_partnerpage_bank_fields.py`
- Updated `core/admin.py` with dedicated fieldsets for each bank
- Updated `templates/core/partner.html` to render fields from DB with fallback to "Add bank details in Admin →" link

**How to update bank details going forward:**

1. Go to `/admin/core/partnerpage/`
2. Fill in `🏦 Bank 1 Details` and `🏦 Bank 2 Details` fieldsets
3. Click Save — changes appear instantly on the live site

---

### 9.4 Contact Us — Email / Phone Configurable from Admin (April 2026)

**How it works:**
The Contact page already pulls phone, email, and WhatsApp from the `SiteSettings` model (single-row config):

1. Go to `/admin/core/sitesettings/`
2. Update `Email`, `Phone Primary`, `Phone Secondary`, `WhatsApp Number`, `Address`
3. Click Save — changes appear on Contact Us page immediately

No code changes needed. The `contact.html` template already uses `{{ site.email }}`, `{{ site.phone_primary }}`, etc. via the `site` context processor.

---

### 9.5 Ijazah Upload Directory Changed (April 2026)

**Symptom:** Ijazah images uploaded to `media/ijazat/` but the model used `upload_to="ijazah/"`.

**Fix applied:** Renamed all references from `ijazat` → `ijazah` in models, views, seed commands, and API URLs.

```bash
# On PythonAnywhere — move any files that landed in old path
mv ~/madinatulilm/media/ijazat/* ~/madinatulilm/media/ijazah/ 2>/dev/null || true
```

---
