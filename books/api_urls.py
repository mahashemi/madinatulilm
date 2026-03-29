from django.urls import path
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import BookCategory, Book
from .serializers import BookCategorySerializer, BookSerializer

app_name = "api_books"

urlpatterns = [
    path("categories/", ListAPIView.as_view(queryset=BookCategory.objects.all(), serializer_class=BookCategorySerializer), name="categories"),
    path("",            ListAPIView.as_view(queryset=Book.objects.filter(is_active=True), serializer_class=BookSerializer), name="list"),
    path("<int:pk>/",   RetrieveAPIView.as_view(queryset=Book.objects.filter(is_active=True), serializer_class=BookSerializer), name="detail"),
]
