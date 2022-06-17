from django.shortcuts import render
from django.http import JsonResponse
from .models import lastModified
import requests


def pkgs_update_status_json(request):
    last_modified = lastModified.objects.all().order_by("arch", "branch", "repo")
    status = list(last_modified.values())
    return JsonResponse({'status': status})


def pkgs_update_status(request):
    url = request.get_raw_uri().replace("status/", "status.json")
    response = requests.get(url)
                   
            
    return render(
        request,
        template_name="status.html",
        context = response.json()
        )
    
