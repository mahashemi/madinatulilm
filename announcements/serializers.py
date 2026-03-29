from rest_framework import serializers
from .models import AnnouncementCategory, Announcement


class AnnouncementCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementCategory
        fields = "__all__"


class AnnouncementSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.title_en", read_only=True)

    class Meta:
        model = Announcement
        fields = "__all__"
