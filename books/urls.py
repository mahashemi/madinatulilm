from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path("",                      views.books_home,        name="home"),
    path("category/<str:slug>/",  views.books_by_category, name="category"),
    path("<int:pk>/",             views.book_detail,       name="detail"),
    path("<int:pk>/download/",    views.book_download,     name="download"),
]
