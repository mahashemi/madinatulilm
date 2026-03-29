from django.shortcuts import render, get_object_or_404
from .models import ShariaCategory, ShariaContent


def sharia_home(request):
    categories = ShariaCategory.objects.all()
    context = {"categories": categories}
    return render(request, "sharia/sharia_home.html", context)


def sharia_category(request, name):
    category = get_object_or_404(ShariaCategory, name=name)
    contents = category.contents.filter(is_active=True)
    return render(request, "sharia/sharia_category.html", {"category": category, "contents": contents})


def sharia_detail(request, pk):
    content = get_object_or_404(ShariaContent, pk=pk, is_active=True)
    return render(request, "sharia/sharia_detail.html", {"content": content})
