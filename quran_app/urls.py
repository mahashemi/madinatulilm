from django.urls import path
from . import views

app_name = "quran"

urlpatterns = [
    path("",          views.quran_home,   name="home"),
    path("<int:pk>/", views.quran_detail, name="detail"),
]
