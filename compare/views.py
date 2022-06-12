#from django.shortcuts import render
from django.http import HttpResponse
from .models import lastModified


def update_status_view(request):
    #TODO views html, bash and json ? if request.GET("format"== "xxx")
    ret = ""
    for item in lastModified.objects.all().values():
        ret = f"{ret}\n{item}"
    return HttpResponse(
                # str(lastModified.objects.all().values())
                ret,
                # contentype='application/json'
            )
