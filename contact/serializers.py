from rest_framework import serializers
from .models import ContactMessage, Question


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "full_name", "email", "phone", "subject", "message", "created_at"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "full_name", "email", "phone", "category", "question", "is_anonymous", "created_at"]


class PublicQASerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ["id", "display_name", "category", "question", "answer", "answered_by", "answer_date"]

    def get_display_name(self, obj):
        return "Anonymous" if obj.is_anonymous else obj.full_name
