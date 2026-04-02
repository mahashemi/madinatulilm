from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("",            views.home,      name="home"),
    path("about/",      views.about,     name="about"),
    path("founder/",    views.founder,   name="founder"),
    path("academics/",  views.academics, name="academics"),
    path("gallery/",    views.gallery,   name="gallery"),
    path("partner/",    views.partner,   name="partner"),
]
