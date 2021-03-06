from django.shortcuts import redirect
from django.conf import settings

def shib(request):
    request.session["login_with"] = "Shibboleth"
    request.session["next"] = request.GET["next"] if "next" in request.GET.keys() else "/"
    return redirect("%s/shib/login" % settings.BASE_ROOT)

def login(request):
    return redirect(request.session["next"])

def logout(request):
    return redirect("%s/" % settings.BASE_ROOT)

