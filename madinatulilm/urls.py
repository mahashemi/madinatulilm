"""
Root URL Configuration — Madrasah Madinatul Ilm
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # CKEditor uploads
    path("ckeditor/", include("ckeditor_uploader.urls")),

    # Public pages
    path("",          include("core.urls",          namespace="core")),
    path("quran/",    include("quran_app.urls",      namespace="quran")),
    path("sharia/",   include("sharia.urls",         namespace="sharia")),
    path("announcements/", include("announcements.urls", namespace="announcements")),
    path("lessons/",  include("lessons.urls",        namespace="lessons")),
    path("books/",    include("books.urls",          namespace="books")),
    path("contact/",  include("contact.urls",        namespace="contact")),

    # REST API (v1)
    path("api/v1/",   include("core.api_urls",       namespace="api_core")),
    path("api/v1/quran/",    include("quran_app.api_urls",   namespace="api_quran")),
    path("api/v1/sharia/",   include("sharia.api_urls",      namespace="api_sharia")),
    path("api/v1/announcements/", include("announcements.api_urls", namespace="api_announcements")),
    path("api/v1/lessons/",  include("lessons.api_urls",     namespace="api_lessons")),
    path("api/v1/books/",    include("books.api_urls",       namespace="api_books")),
    path("api/v1/contact/",  include("contact.api_urls",     namespace="api_contact")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
