"""
Management command: python manage.py create_superuser
Creates the default admin superuser if one does not already exist.
Override with env vars: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create default superuser (safe to run multiple times)"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email    = os.environ.get("DJANGO_SUPERUSER_EMAIL",    "admin@madinatulilm.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "MIL@admin2026!")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"  · Superuser already exists: {username}"))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"  ✓ Superuser created: {username}"))

        self.stdout.write(f"\n  → Admin panel: http://127.0.0.1:8000/admin/")
        self.stdout.write(f"  → Username : {username}")
        self.stdout.write(f"  → Password : {password}\n")
