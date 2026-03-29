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

## 3. Full Fresh Deployment (New Server)

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

# Seed all initial content (trustees, ijazat, programs, categories, etc.)
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
