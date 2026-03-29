from django.urls import path
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import AnnouncementCategory, Announcement
from .serializers import AnnouncementCategorySerializer, AnnouncementSerializer

app_name = "api_announcements"

urlpatterns = [
    path("categories/", ListAPIView.as_view(queryset=AnnouncementCategory.objects.all(), serializer_class=AnnouncementCategorySerializer), name="categories"),
    path("",            ListAPIView.as_view(queryset=Announcement.objects.filter(is_active=True), serializer_class=AnnouncementSerializer), name="list"),
    path("<int:pk>/",   RetrieveAPIView.as_view(queryset=Announcement.objects.filter(is_active=True), serializer_class=AnnouncementSerializer), name="detail"),
]
