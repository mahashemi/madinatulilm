from rest_framework import serializers
from .models import ShariaCategory, ShariaContent


class ShariaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShariaCategory
        fields = "__all__"


class ShariaContentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.title_en", read_only=True)

    class Meta:
        model = ShariaContent
        fields = "__all__"
