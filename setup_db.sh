#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
#  Madrasah Madinatul Ilm — Database Setup Script (PythonAnywhere)
#  Run this ONCE from the project root (where manage.py lives):
#
#    cd /home/madrasahmadinatulilm/mohammadiyyahtrust
#    bash setup_db.sh
#
#  Prerequisites (already done on PythonAnywhere):
#    - Django 5.1.3 installed (pip install -r requirements.txt)
#    - .env file present with MySQL credentials
#    - MySQL database created on PythonAnywhere
# ═══════════════════════════════════════════════════════════════════════════════

set -e

GREEN='\033[0;32m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'
ok()  { echo -e "${GREEN}[OK]${NC}  $*"; }
log() { echo -e "${CYAN}[>>]${NC}  $*"; }
err() { echo -e "${RED}[ERR]${NC} $*"; exit 1; }

[ -f "manage.py" ] || err "Run from the project root — manage.py not found."

echo ""
echo -e "${CYAN}══════════════════════════════════════════${NC}"
echo -e "${CYAN}  Madrasah Madinatul Ilm — DB Setup       ${NC}"
echo -e "${CYAN}══════════════════════════════════════════${NC}"
echo ""

# ── 1. Migrations ──────────────────────────────────────────────────────────────
log "Running migrations ..."
python manage.py migrate --noinput
ok "Migrations complete"

# ── 2. Seed core content ──────────────────────────────────────────────────────
log "Seeding site content (trustees, ijazah, programs, biographies, gallery) ..."
python manage.py seed_content
ok "seed_content done"

# ── 3. Seed hadiths & partner page ───────────────────────────────────────────
log "Seeding hadiths and partner page ..."
python manage.py seed_hadiths
ok "seed_hadiths done"

# ── 4. Seed useful links ──────────────────────────────────────────────────────
log "Seeding useful Islamic resource links ..."
python manage.py seed_useful_links
ok "seed_useful_links done"

# ── 5. Create admin superuser ─────────────────────────────────────────────────
log "Creating admin superuser ..."
# To use custom credentials, export these before running the script:
#   export DJANGO_SUPERUSER_USERNAME=minhal
#   export DJANGO_SUPERUSER_EMAIL=admin@madinatulilm.com
#   export DJANGO_SUPERUSER_PASSWORD='YourNewPassword!'
python manage.py create_superuser
ok "Superuser ready"

# ── 6. Collect static files ───────────────────────────────────────────────────
log "Collecting static files ..."
python manage.py collectstatic --noinput --clear
ok "Static files collected"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}══════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅  Database setup complete!             ${NC}"
echo -e "${GREEN}══════════════════════════════════════════${NC}"
echo ""
echo -e "  Admin panel : https://madrasahmadinatulilm.pythonanywhere.com/admin/"
echo -e "  Username    : ${DJANGO_SUPERUSER_USERNAME:-admin}"
echo -e "  Password    : ${DJANGO_SUPERUSER_PASSWORD:-MIL@admin2026!}"
echo ""
echo -e "  ⚠  Go to Admin → Users → admin → Change password after first login."
echo ""
