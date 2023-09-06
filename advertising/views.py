from django.http import JsonResponse
from .models import Advert
from django.core.serializers import serialize
import json


def ads_json(request):        
    ads = Advert.objects.all()
    serialized_data = serialize("json", ads)
    serialized_data = json.loads(serialized_data)

    affiliates = []
    for ad in serialized_data:
        data = ad["fields"]
        template = {
        "title": data["title"],
        "url": data["url"],
        "img": data["image"],
        "desc": data["description"],
        }
        affiliates.append(template)

    return JsonResponse(affiliates, safe=False)



