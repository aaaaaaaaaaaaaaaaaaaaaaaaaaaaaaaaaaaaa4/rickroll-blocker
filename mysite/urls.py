"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from urllib.parse import (urlencode, unquote, urlparse, parse_qsl, ParseResult)
from urllib.parse import urlparse as theurlparse
import base64
from django.views.decorators.csrf import csrf_exempt
from .links import links
import urlexpander
import validators
import re
urlreg = re.compile(r"https?://(www\.)?")
regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
    r'localhost|'  #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE)


@csrf_exempt
def yesorno(request):
    thetesturl = request.GET.get("url")
    if not validators.url(thetesturl):
        response = {"status": False, "data": {"error": "not a url"}}
        return JsonResponse(response,
                            json_dumps_params={'indent': 2},
                            status=200)
    if "latLmes" in thetesturl:
        response = {
            "status": True,
            "data": {
                "url": "latLmes.com",
                "rickroll": True
            }
        }
        return JsonResponse(response, json_dumps_params={'indent': 2})

    testurl = urlexpander.expand(thetesturl).replace("www.", "")
    query = urlparse(testurl)
    path = query.path
    if query.hostname == "rickroll-links-database.ch1ck3n.repl.co":
        response = {
            "status": True,
            "data": {
                "url": "repl.co",
                "rickroll": False
            }
        }
        return JsonResponse(response, json_dumps_params={'indent': 2})
    if query.hostname == "theraleighregister.com":
        response = {
            "status": True,
            "data": {
                "url": "theraleighregister.com",
                "rickroll": "true"
            }
        }
        return JsonResponse(response, json_dumps_params={'indent': 2})
    if path == "/":
        path == ""
    if query.query:
        print(query.query)
        path = path + "?" + query.query
    hostname = str(query.hostname)
    if hostname == "None":
        hostname = ""
    response = {
        "status": True,
        "data": {
            "url": str(hostname) + str(path),
            "rickroll": str(str(hostname) + str(path) in links)
        }
    }
    return JsonResponse(response, json_dumps_params={'indent': 2})


def add_url_params(url, params):
    url_parts = list(theurlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)

    return theurlparse.urlunparse(url_parts)


def attemptedrickroll(request):
    url = request.GET.get("url")
    newurl = url
    return render(request, "rickroll.html", {
        "url": str(base64.b64decode(request.GET.get("url"))),
        "risktaken": newurl
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: render(request, "index.html")),
    path('yesorno/', yesorno),
    path("bwah/", attemptedrickroll),
    path("install/",
         lambda request: render(request, "install.html"),
         name="install")
]
