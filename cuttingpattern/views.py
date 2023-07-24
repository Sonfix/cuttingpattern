from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Customer, User, CuttingPattern
from .api import Api

def index(request):
    if request.user.is_authenticated:
        usr= User.objects.get(pk=request.user.id)
        return render(request, "cuttingpattern/index.html", {
            "cuttingpatterns" : usr.cuttingpatterns.all()
        })
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
def ApiCommand(request, func_name):
    '''
        Returns the given command result in json format
    '''
    return Api().resolve_command(func_name, request)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cuttingpattern/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cuttingpattern/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cuttingpattern/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cuttingpattern/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cuttingpattern/register.html")

def show_cuttingpatttern(request, id):
    cp = CuttingPattern.objects.get(pk = id)
    if cp:
        return render(request, "cuttingpattern/cuttingpattern.html", {
            "pattern" : cp
        })
    else:
        return HttpResponseRedirect(reverse("index"))

def explore(request):
    cs = Customer.objects.all()
    return render(request, "cuttingpattern/explore.html", {
        "customers" : cs
    })