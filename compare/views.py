from django.http import JsonResponse
from .models import lastModified, PackageModel
from django.core.serializers import serialize
import json

def pkgs_update_status_json(request):
    last_modified = lastModified.objects.all().order_by("arch", "branch", "repo")
    status = list(last_modified.values())
    return JsonResponse({'status': status})

def pkgs_json(request):
    #context = super().get_context(request)
    search_query = request.GET.get('query', None)
    arm = request.GET.get('arm', None)
    if arm:
        arch = "aarch64"
    else:
        arch = "x86_64"

    if search_query:
        search_results = PackageModel.objects.all().filter(name__contains=search_query.lower(), arch=arch)
    else:
        search_results = PackageModel.objects.none()

    serialized_data = serialize("json", search_results)
    serialized_data = json.loads(serialized_data)
    return JsonResponse(serialized_data, safe=False)