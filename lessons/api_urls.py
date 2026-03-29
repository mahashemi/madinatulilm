from django.urls import path
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Subject, LessonSeries, Lesson
from .serializers import SubjectSerializer, LessonSeriesSerializer, LessonSerializer

app_name = "api_lessons"

urlpatterns = [
    path("subjects/",         ListAPIView.as_view(queryset=Subject.objects.filter(is_active=True), serializer_class=SubjectSerializer), name="subjects"),
    path("series/",           ListAPIView.as_view(queryset=LessonSeries.objects.filter(is_active=True), serializer_class=LessonSeriesSerializer), name="series-list"),
    path("series/<int:pk>/",  RetrieveAPIView.as_view(queryset=LessonSeries.objects.filter(is_active=True), serializer_class=LessonSeriesSerializer), name="series-detail"),
    path("",                  ListAPIView.as_view(queryset=Lesson.objects.filter(is_active=True), serializer_class=LessonSerializer), name="lesson-list"),
    path("<int:pk>/",         RetrieveAPIView.as_view(queryset=Lesson.objects.filter(is_active=True), serializer_class=LessonSerializer), name="lesson-detail"),
]
