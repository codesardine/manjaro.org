import urllib.request
from urllib.request import ssl, socket
import datetime
import json
import concurrent.futures
from django.shortcuts import render
from django.http import HttpResponse


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
                certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
                delta = certExpires - now
                certificates.append({
                    "url": url,
                    "date": certExpires,
                    "delta": delta.days
                })


    return render(request, 'wagtailforum/certifs.html', {
        'certifs': certificates,
    })

def index(request):

    branch = request.GET.get('branch', "stable")
    if branch not in ("stable", "testing", "unstable"):
        branch = "stable"

    with urllib.request.urlopen(f"https://forum.manjaro.org/c/announcements/{branch}-updates.json") as f_url:
        req = f_url.read()

    # doc: https://docs.discourse.org/#tag/Categories
    topics = json.loads(req)['topic_list']['topics']
    topics = [t for t in topics if not t['title'].startswith('About')][0:12]  # limit 12 / 30

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures.append(executor.map(_get_subject, topics))

    return render(request, 'wagtailforum/certifs.html', {
        'branch': branch,
        'topics': topics,
    })


def _get_subject(topic):
    """read one subject"""
    with urllib.request.urlopen(f"https://forum.manjaro.org/t/{topic['id']}.json") as f_url:
        req = f_url.read()
    post = json.loads(req)['post_stream']['posts'][0]
    topic['voters'] = post['polls'][0]['voters']
    topic['poll_ok'] = post['polls'][0]['options'][0]['votes']
    pourcentage = round((post['polls'][0]['options'][0]['votes'] / post['polls'][0]['voters']) * 100)
    topic['poll_pourcent'] = 100 - pourcentage
    topic['poll_thanks'] = post['polls'][0]['options'][1]['votes']
    topic['poll_opps'] = post['polls'][0]['options'][2]['votes']
