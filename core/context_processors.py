from .models import SiteSettings


def site_info(request):
    """Inject site settings into every template context."""
    try:
        settings_obj = SiteSettings.objects.first()
    except Exception:
        settings_obj = None
    return {"site": settings_obj}
