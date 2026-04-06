# Remote Server Access — PythonAnywhere
## Madrasah Madinatul Ilm · www.muhammadiyyahtrust.org

---

## 1. Server Details

| Item | Value |
|------|-------|
| **Host** | `ssh.pythonanywhere.com` |
| **Port** | `22` (standard SSH) |
| **Username** | `madrasahmadinatulilm` |
| **Password** | stored in `.env` / credential manager |
| **Site domain** | `www.muhammadiyyahtrust.org` |
| **Project root** | `~/madinatulilm/` |
| **Python** | `/home/madrasahmadinatulilm/.local/bin/python3` (Python 3.13.1) |
| **Virtualenv** | ❌ No separate venv — Django installed to user `.local` via `pip install --user` |
| **WSGI file** | `/var/www/www_muhammadiyyahtrust_org_wsgi.py` |

> **Note:** The standard `~/.virtualenvs/` directory exists but is empty hooks only.
> The actual Django installation lives in `~/.local/lib/python3.13/`.
> Always invoke `python3` directly (not `workon` or `source activate`).

---

## 2. SSH Access (from your Mac)

### Prerequisite — install sshpass
```bash
brew install hudochenkov/sshpass/sshpass
```

### Basic SSH session (interactive)
```bash
ssh madrasahmadinatulilm@ssh.pythonanywhere.com
# Enter password when prompted
```

### One-liner non-interactive command
```bash
sshpass -p 'YOUR_PASSWORD' ssh -o StrictHostKeyChecking=no \
  madrasahmadinatulilm@ssh.pythonanywhere.com \
  'COMMAND_HERE'
```

> ⚠️ PythonAnywhere blocks rapid repeated SSH connections — if you get
> `Too many authentication failures`, wait ~60 seconds before retrying.

---

## 3. Standard Deploy Workflow

After pushing code to GitHub, run this **complete deploy sequence**:

```bash
# ── 1. Pull latest code ────────────────────────────────────
sshpass -p 'PASSWORD' ssh -o StrictHostKeyChecking=no \
  madrasahmadinatulilm@ssh.pythonanywhere.com \
  'cd ~/madinatulilm && git pull origin main 2>&1'

# ── 2. Apply Django migrations ─────────────────────────────
sshpass -p 'PASSWORD' ssh -o StrictHostKeyChecking=no \
  madrasahmadinatulilm@ssh.pythonanywhere.com \
  'cd ~/madinatulilm && python3 manage.py migrate --no-input 2>&1'

# ── 3. Collect static files (if static assets changed) ─────
sshpass -p 'PASSWORD' ssh -o StrictHostKeyChecking=no \
  madrasahmadinatulilm@ssh.pythonanywhere.com \
  'cd ~/madinatulilm && python3 manage.py collectstatic --no-input 2>&1'

# ── 4. Reload the web app ──────────────────────────────────
# Option A — via PythonAnywhere REST API (requires API token in .env)
curl -s -X POST \
  "https://www.pythonanywhere.com/api/v0/user/madrasahmadinatulilm/webapps/www.muhammadiyyahtrust.org/reload/" \
  -H "Authorization: Token YOUR_PA_API_TOKEN"

# Option B — touch the WSGI file (requires write permission)
sshpass -p 'PASSWORD' ssh -o StrictHostKeyChecking=no \
  madrasahmadinatulilm@ssh.pythonanywhere.com \
  'touch /var/www/www_muhammadiyyahtrust_org_wsgi.py'

# Option C — MANUAL (always works)
#   → Log into https://www.pythonanywhere.com
#   → Web tab → www.muhammadiyyahtrust.org → green Reload button
```

### Combined one-liner (pull + migrate + reload via API)
```bash
sshpass -p 'PASSWORD' ssh -o StrictHostKeyChecking=no \
  madrasahmadinatulilm@ssh.pythonanywhere.com \
  'cd ~/madinatulilm && git pull origin main && python3 manage.py migrate --no-input' \
  && curl -s -X POST \
  "https://www.pythonanywhere.com/api/v0/user/madrasahmadinatulilm/webapps/www.muhammadiyyahtrust.org/reload/" \
  -H "Authorization: Token YOUR_PA_API_TOKEN"
```

---

## 4. PythonAnywhere REST API

Generate a token at: **https://www.pythonanywhere.com/user/madrasahmadinatulilm/account/#api_token**

Save it in `.env`:
```
PA_API_TOKEN=your_token_here
```

### Useful API endpoints

```bash
BASE="https://www.pythonanywhere.com/api/v0/user/madrasahmadinatulilm"
TOKEN="Authorization: Token YOUR_TOKEN"

# Reload webapp
curl -s -X POST "$BASE/webapps/www.muhammadiyyahtrust.org/reload/" -H "$TOKEN"

# List webapps
curl -s "$BASE/webapps/" -H "$TOKEN" | python3 -m json.tool

# Check webapp status
curl -s "$BASE/webapps/www.muhammadiyyahtrust.org/" -H "$TOKEN" | python3 -m json.tool
```

---

## 5. Useful Remote Commands

```bash
# Check Django version / import works
python3 -c "import django; print(django.__version__)"

# Show pending migrations
cd ~/madinatulilm && python3 manage.py showmigrations

# Run management command (e.g. seed content)
cd ~/madinatulilm && python3 manage.py seed_content

# Create superuser
cd ~/madinatulilm && python3 manage.py create_superuser

# Tail the error log (last 50 lines)
tail -50 /var/log/madrasahmadinatulilm.pythonanywhere.com.error.log

# Check server error log
cat /var/log/madrasahmadinatulilm.pythonanywhere.com.error.log | grep -i "error\|traceback" | tail -20

# Find all virtualenvs / Python installs
find ~ -name "activate" -maxdepth 6 2>/dev/null
which python3 && python3 --version
```

---

## 6. File Locations on Server

```
/home/madrasahmadinatulilm/
├── madinatulilm/              ← Django project root (git repo)
│   ├── manage.py
│   ├── static/                ← static source files
│   ├── media/                 ← uploaded media (NOT in git)
│   ├── templates/
│   └── madinatulilm/
│       ├── settings.py
│       └── wsgi.py
├── .local/
│   └── bin/
│       └── python3            ← system Python (3.13.1)
└── .virtualenvs/              ← empty (hooks only, no active venv)

/var/www/
└── www_muhammadiyyahtrust_org_wsgi.py   ← touch this to reload

/var/log/
└── madrasahmadinatulilm.pythonanywhere.com.error.log   ← Django errors
```

---

## 7. Known Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| `No such file: activate` | No virtualenv on this server | Use `python3` directly |
| `Too many authentication failures` | SSH rate limiting | Wait 60s, retry |
| Static files not updating | Browser/CDN cache | Hard refresh or `collectstatic` |
| Admin 500 after migration | Migration not run on server | `python3 manage.py migrate` |
| WSGI touch permission denied | File owned by www-data | Use PA API or manual reload in dashboard |

---

## 8. Quick Reference Card

```bash
# SSH password login
ssh madrasahmadinatulilm@ssh.pythonanywhere.com

# Non-interactive with sshpass
sshpass -p 'PASSWORD' ssh -o StrictHostKeyChecking=no \
  madrasahmadinatulilm@ssh.pythonanywhere.com 'COMMAND'

# Python on server
python3 manage.py COMMAND          # from ~/madinatulilm/

# Reload via API
curl -X POST https://www.pythonanywhere.com/api/v0/user/madrasahmadinatulilm/webapps/www.muhammadiyyahtrust.org/reload/ \
  -H "Authorization: Token TOKEN"

# Manual reload
# → pythonanywhere.com → Web tab → Reload ✅
```
