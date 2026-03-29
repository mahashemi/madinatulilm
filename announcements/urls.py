from django.urls import path
from . import views

app_name = "announcements"

urlpatterns = [
    path("",               views.announcements_home,        name="home"),
    path("<str:slug>/",    views.announcements_by_category, name="category"),
    path("detail/<int:pk>/", views.announcement_detail,     name="detail"),
]
