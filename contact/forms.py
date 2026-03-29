from django import forms
from .models import ContactMessage, Question


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "phone", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Full Name"}),
            "email":     forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}),
            "phone":     forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Phone (optional)"}),
            "subject":   forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
            "message":   forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Your message..."}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["full_name", "email", "phone", "category", "question", "is_anonymous"]
        widgets = {
            "full_name":    forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Full Name"}),
            "email":        forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}),
            "phone":        forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Phone (optional)"}),
            "category":     forms.Select(attrs={"class": "form-select"}),
            "question":     forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Your question..."}),
            "is_anonymous": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
