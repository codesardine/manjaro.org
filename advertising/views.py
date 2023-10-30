from django.http import JsonResponse
from .models import Advert
from django.core.serializers import serialize
import json
from wagtail.images import get_image_model


def ads_json(request):        
    ads = Advert.objects.all()
    serialized_data = serialize("json", ads)
    serialized_data = json.loads(serialized_data)
    img_model = get_image_model()

    affiliates = []
    for ad in serialized_data:
        data = ad["fields"]
        hidden = data["hidden"]
        if not hidden:
            img = img_model.objects.filter(id=data["image"])[0]
            template = {
            "title": data["title"],
            "url": data["url"],
            "img": img.renditions.all()[1].url,
            "desc": data["description"],
            }
            affiliates.append(template)

    return JsonResponse(affiliates, safe=False)



