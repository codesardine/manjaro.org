from django.http import JsonResponse
from .models import lastModified


def pkgs_update_status_json(request):
    last_modified = lastModified.objects.all().order_by("arch", "branch", "repo")
    status = list(last_modified.values())
    return JsonResponse({'status': status})   
