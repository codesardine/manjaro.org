#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from .models import lastModified, Archs
from .packages import Branches

def c_html(index: int, values):
    count = values[index]
    if count < 10:
        count = f'<span style="color:red">{count}</span>'
    return f'<td align="right">{count}</td>'

def update_status(request):
    #TODO views html, bash and json ? if request.GET("format"== "xxx")
    format_out = request.GET.get('format', 'json')
    items = lastModified.objects.all().order_by("arch", "branch", "repo")
    if format_out == "txt":
        rets = []
        for item in items:
            try:
                date_str = item.date.strftime('%Y-%d-%m,%Hh:%M')
            except AttributeError:
                date_str = ""
            rets.append(f"{item.arch:12}{item.branch:18}{item.repo:16}{date_str:18} {item.status}")
        return HttpResponse(
                '\n'.join(rets)
            )
    elif format_out == "html":
        rets = []
        sep = '</td><td>'
        for item in items:
            try:
                date_str = item.date.strftime('%Y-%d-%m,%Hh:%M')
            except AttributeError:
                date_str = ""
            rets.append(f"<tr><td>{item.arch}{sep}{item.branch}{sep}{item.repo}{sep}{date_str}</td><th>{item.status}</th></tr>")
        report = '<table cellspacing="6">' + '\n'.join(rets) + "</table><hr>"
        rets = ['<table cellspacing="6">']
        rets.append('<tr><td colspan="2"></td><td>stable</td><td>testing</td><td>unstable</td></tr>')
        with connection.cursor() as cursor:
            sql = '''SELECT architecture, repo,
                    sum(CASE WHEN (stable) != "" THEN 1 ELSE 0 END)  as stables,
                    sum(CASE WHEN (testing) != "" THEN 1 ELSE 0 END)  as testings,
                    sum(CASE WHEN (unstable) != "" THEN 1 ELSE 0 END)  as unstables
                    FROM compare_packagemodel
                    GROUP BY repo, architecture
                    order by architecture;'''
            for item in cursor.execute(sql):
                rets.append(f'<tr><td>{Archs(item[0]).name}</td><td>{item[1]}</td>{c_html(2, item)}{c_html(3, item)}{c_html(4, item)}</tr>')
        rets.append('</table>')
        return HttpResponse(
                report + '' + '\n'.join(rets) + ""
            )
    else:
        status = list(items.values())
        return JsonResponse({'status': status})
