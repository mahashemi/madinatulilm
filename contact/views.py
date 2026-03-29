from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage, Question
from .forms import ContactForm, QuestionForm


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ip_address = request.META.get("REMOTE_ADDR")
            msg.save()
            messages.success(request, "Your message has been received. We will respond shortly, in sha Allah.")
            return redirect("contact:contact")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})


def ask_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.ip_address = request.META.get("REMOTE_ADDR")
            q.save()
            messages.success(request, "Your question has been submitted. We will answer it soon, in sha Allah.")
            return redirect("contact:ask")
    else:
        form = QuestionForm()

    public_qas = Question.objects.filter(is_public=True, status="answered").order_by("-answer_date")[:10]
    return render(request, "contact/ask_question.html", {"form": form, "public_qas": public_qas})
