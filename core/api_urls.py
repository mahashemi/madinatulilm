from django.urls import path
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import (
    SiteSettings, WelcomeSection, MissionSection, VisionSection,
    AboutSection, Founder, Ijazah, Trustee, AcademicProgram, MadrasahGallery
)
from .serializers import (
    SiteSettingsSerializer, WelcomeSectionSerializer, MissionSerializer,
    VisionSerializer, AboutSerializer, FounderSerializer, IjazahSerializer,
    TrusteeSerializer, AcademicProgramSerializer, GallerySerializer
)

app_name = "api_core"

urlpatterns = [
    path("settings/",  ListAPIView.as_view(queryset=SiteSettings.objects.all(),        serializer_class=SiteSettingsSerializer),   name="settings"),
    path("welcome/",   ListAPIView.as_view(queryset=WelcomeSection.objects.filter(is_active=True), serializer_class=WelcomeSectionSerializer), name="welcome"),
    path("mission/",   ListAPIView.as_view(queryset=MissionSection.objects.filter(is_active=True), serializer_class=MissionSerializer), name="mission"),
    path("vision/",    ListAPIView.as_view(queryset=VisionSection.objects.filter(is_active=True),  serializer_class=VisionSerializer), name="vision"),
    path("about/",     ListAPIView.as_view(queryset=AboutSection.objects.filter(is_active=True),   serializer_class=AboutSerializer),  name="about"),
    path("founder/",   ListAPIView.as_view(queryset=Founder.objects.filter(is_active=True),        serializer_class=FounderSerializer), name="founder"),
    path("ijazat/",    ListAPIView.as_view(queryset=Ijazah.objects.all(),              serializer_class=IjazahSerializer),        name="ijazat"),
    path("trustees/",  ListAPIView.as_view(queryset=Trustee.objects.filter(is_active=True),        serializer_class=TrusteeSerializer), name="trustees"),
    path("programs/",  ListAPIView.as_view(queryset=AcademicProgram.objects.filter(is_active=True),serializer_class=AcademicProgramSerializer), name="programs"),
    path("gallery/",   ListAPIView.as_view(queryset=MadrasahGallery.objects.filter(is_active=True),serializer_class=GallerySerializer),name="gallery"),
]
