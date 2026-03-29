from django.shortcuts import render, get_object_or_404
from .models import QuranResource


def quran_home(request):
    resource_type = request.GET.get("type", "")
    resources = QuranResource.objects.filter(is_active=True)
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    context = {
        "resources": resources,
        "resource_type": resource_type,
        "resource_types": QuranResource.RESOURCE_TYPE,
    }
    return render(request, "quran_app/quran_home.html", context)


def quran_detail(request, pk):
    resource = get_object_or_404(QuranResource, pk=pk, is_active=True)
    return render(request, "quran_app/quran_detail.html", {"resource": resource})
