from django.contrib import admin
from .models import Subject, LessonSeries, Lesson


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title_en", "slug", "is_active", "sort_order")
    list_editable = ("sort_order", "is_active")


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ("lesson_number", "title_en", "media_type", "is_active")


@admin.register(LessonSeries)
class LessonSeriesAdmin(admin.ModelAdmin):
    list_display = ("title_en", "subject", "instructor", "is_active", "created_at")
    list_filter = ("subject", "is_active")
    list_editable = ("is_active",)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title_en", "series", "lesson_number", "media_type", "is_active")
    list_filter = ("series__subject", "media_type", "is_active")
    list_editable = ("is_active",)
    search_fields = ("title_en", "title_ar")
