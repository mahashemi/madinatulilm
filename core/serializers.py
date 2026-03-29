from rest_framework import serializers
from .models import (
    SiteSettings, WelcomeSection, MissionSection, VisionSection,
    AboutSection, Founder, Ijazah, Trustee, AcademicProgram, MadrasahGallery
)


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        exclude = ["id"]


class WelcomeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomeSection
        fields = "__all__"


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionSection
        fields = "__all__"


class VisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisionSection
        fields = "__all__"


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = "__all__"


class FounderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Founder
        fields = "__all__"


class IjazahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ijazah
        fields = "__all__"


class TrusteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trustee
        fields = "__all__"


class AcademicProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicProgram
        fields = "__all__"


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MadrasahGallery
        fields = "__all__"
