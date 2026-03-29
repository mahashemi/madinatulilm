from rest_framework import serializers
from .models import Subject, LessonSeries, Lesson


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonSeriesSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.title_en", read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = LessonSeries
        fields = "__all__"
