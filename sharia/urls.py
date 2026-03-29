from django.urls import path
from . import views

app_name = "sharia"

urlpatterns = [
    path("",                views.sharia_home,     name="home"),
    path("<str:name>/",     views.sharia_category, name="category"),
    path("detail/<int:pk>/",views.sharia_detail,   name="detail"),
]
