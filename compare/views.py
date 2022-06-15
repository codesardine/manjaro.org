#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import lastModified


def update_status(request):
    #TODO views html, bash and json ? if request.GET("format"== "xxx")
    format_out = request.GET.get('format', 'json')
    items = lastModified.objects.all().order_by("arch", "branch", "repo")
    if format_out == "txt":
        rets = []
        for item in items:
            rets.append(f"{item.arch:12}{item.branch:18}{item.repo:16}{item.date.strftime('%Y-%d-%m,%Hh:%M'):18} {item.status}")
        return HttpResponse(
                '\n'.join(rets)
            )
    elif format_out == "html":
        rets = []
        sep = '</td><td>'
        for item in items:
            rets.append(f"<tr><td>{item.arch}{sep}{item.branch}{sep}{item.repo}{sep}{item.date.strftime('%Y-%d-%m,%Hh:%M')}</td><th>{item.status}</th></tr>")
        return HttpResponse(
                '<table cellspacing="6">' + '\n'.join(rets) + "</table>"
            )
    else:
        status = list(items.values())
        return JsonResponse({'status' : status})
