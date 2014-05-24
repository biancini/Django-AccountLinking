from django.shortcuts import redirect

def shib(request):
    request.session["login_with"] = "Shibboleth"
    request.session["next"] = request.GET["next"] if "next" in request.GET.keys() else "/"
    return redirect("/shib/login")

def login(request):
    return redirect(request.session["next"])

def logout(request):
    return redirect("/")

