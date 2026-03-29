from django.contrib import admin
from .models import ContactMessage, Question


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "status", "created_at")
    list_filter = ("status",)
    list_editable = ("status",)
    search_fields = ("full_name", "email", "subject")
    readonly_fields = ("ip_address", "created_at")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "category", "status", "is_public", "answered_by", "created_at")
    list_filter = ("category", "status", "is_public")
    list_editable = ("status", "is_public")
    search_fields = ("full_name", "question")
    readonly_fields = ("ip_address", "created_at")
    fieldsets = (
        ("Question", {"fields": ("full_name", "email", "phone", "category", "question", "is_anonymous", "ip_address", "created_at")}),
        ("Answer", {"fields": ("status", "is_public", "answered_by", "answer", "answer_date")}),
    )
