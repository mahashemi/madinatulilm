from django.urls import path
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import QuranResource
from .serializers import QuranResourceSerializer

app_name = "api_quran"

urlpatterns = [
    path("",          ListAPIView.as_view(queryset=QuranResource.objects.filter(is_active=True), serializer_class=QuranResourceSerializer), name="list"),
    path("<int:pk>/", RetrieveAPIView.as_view(queryset=QuranResource.objects.filter(is_active=True), serializer_class=QuranResourceSerializer), name="detail"),
]
