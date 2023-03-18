from django.shortcuts import render


def merch(request):
    
    return render(request, 'home/merchandise.html', {
        'certifs': "h",
    })
