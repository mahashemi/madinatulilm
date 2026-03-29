from rest_framework import serializers
from .models import BookCategory, Book


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.title_en", read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
