from django.http import JsonResponse
from .models import Archs, lastModified, RepportPackages
import requests


def pkgs_update_status_json(request):
    last_modified = lastModified.objects.all().order_by("arch", "branch", "repo")
    status = list(last_modified.values())
    return JsonResponse({'status': status})


def pkgs_status(request):
    repport = RepportPackages()
    repport.request()
    return render(
        request,
        template_name="status_pkgs.html",
        context={
            "archs": (a for a in Archs),
            "repport": repport,
        }
        )
