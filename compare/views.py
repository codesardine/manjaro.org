#from django.shortcuts import render
from django.http import HttpResponse
from .models import lastModified


def update_status_view(request):
    #TODO views html, bash and json ? if request.GET("format"== "xxx")
    rets = []
    nl = ',\n'
    for item in lastModified.objects.all().values():
        rets.append(f"{item}")
    return HttpResponse(
                # str(lastModified.objects.all().values())
                f"[\n{nl.join(rets)})\n]",
                headers={
                    'Content-Type': 'application/json',
                }
            )
