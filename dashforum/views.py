from urllib.request import ssl, socket
import datetime
import json
from django.shortcuts import render


def certificates(request):
    hostname = 'manjaro.org'
    port = '443'
    dns = (
        "aur", "blog", "download", "forum",
        "mirrors", "packages", "ping",
        "software", "wiki", "www",
    )
    dns = sorted(set(dns))
    now = datetime.datetime.now()
    certificates = []

    for url in dns:
        url = f"{url}.{hostname}"
        ssl_context = ssl.create_default_context()
        
        with socket.create_connection((url, port)) as sock:
            with ssl_context.wrap_socket(sock, server_hostname=url) as ssock:
                certificate = ssock.getpeercert()
                try:
                    certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    delta = certExpires - now
                    certificates.append({
                        "url": url,
                        "date": certExpires,
                        "delta": delta.days
                    })
                except ValueError as e:
                    print(e, certificate)


    return render(request, 'wagtailforum/certifs.html', {
        'certifs': certificates,
    })
