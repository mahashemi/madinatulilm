from django.urls import path
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import ShariaCategory, ShariaContent
from .serializers import ShariaCategorySerializer, ShariaContentSerializer

app_name = "api_sharia"

urlpatterns = [
    path("categories/",   ListAPIView.as_view(queryset=ShariaCategory.objects.all(), serializer_class=ShariaCategorySerializer), name="categories"),
    path("",              ListAPIView.as_view(queryset=ShariaContent.objects.filter(is_active=True), serializer_class=ShariaContentSerializer), name="list"),
    path("<int:pk>/",     RetrieveAPIView.as_view(queryset=ShariaContent.objects.filter(is_active=True), serializer_class=ShariaContentSerializer), name="detail"),
]
