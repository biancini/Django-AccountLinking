from djangomako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

def login(request):
  args = {
    "next": request.GET["next"] if "next" in request.GET.keys() else "/"
  }
  return render_to_response("choselogin.mako", args)

@login_required
def home(request):
  args = {
    "user": request.user,
    "login_date": request.session["login_date"],
    "login_method": request.session["login_method"]
  }
  return render_to_response("home.mako", args)
