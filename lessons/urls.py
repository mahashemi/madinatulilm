from django.urls import path
from . import views

app_name = "lessons"

urlpatterns = [
    path("",                    views.lessons_home,          name="home"),
    path("<str:slug>/",         views.lessons_by_subject,    name="subject"),
    path("series/<int:pk>/",    views.lesson_series_detail,  name="series"),
    path("lesson/<int:pk>/",    views.lesson_detail,         name="detail"),
]
