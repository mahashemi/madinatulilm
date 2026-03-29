from django.shortcuts import render, get_object_or_404
from .models import Subject, LessonSeries, Lesson


def lessons_home(request):
    subjects = Subject.objects.filter(is_active=True)
    context = {"subjects": subjects}
    return render(request, "lessons/lessons_home.html", context)


def lessons_by_subject(request, slug):
    subject = get_object_or_404(Subject, slug=slug, is_active=True)
    series_list = subject.series.filter(is_active=True)
    return render(request, "lessons/lessons_subject.html", {"subject": subject, "series_list": series_list})


def lesson_series_detail(request, pk):
    series = get_object_or_404(LessonSeries, pk=pk, is_active=True)
    lessons = series.lessons.filter(is_active=True)
    return render(request, "lessons/lesson_series.html", {"series": series, "lessons": lessons})


def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk, is_active=True)
    return render(request, "lessons/lesson_detail.html", {"lesson": lesson})
