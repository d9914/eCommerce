from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing


def index(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True),
        "category": all_categories
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        category = Category.objects.get(
            categorgy_name=request.POST["category"])
        l = Listing(title=request.POST["title"], image=request.POST["image"],
                    description=request.POST["description"], price=request.POST["price"], owner=request.user, category=category)
        l.save()
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all()
        })
    else:
        all_categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "category": all_categories
        })


def listing(request, id):
    if request.method == "GET":
        l = Listing.objects.get(id=id, is_active=True, )
        return render(request, "auctions/listing.html", {
            "listings": l
        })
    else:
        l = Listing.objects.get(id=id)
        bid = float(request.POST["bid"])
        if bid > l.price:
            l.price = bid
            l.save()
            return render(request, "auctions/listing.html", {
                "listings": l
            })
        else:
            return render(request, "auctions/error.html", {
                "message": "INVALID BID"
            })


def error(request):
    return render(request, "auctions/error.html")


def display_category(request):
    if request.method == "POST":
        category = request.POST["category"]
        category = Category.objects.get(category_name=category)
        l = Listing.objects.filter(is_active=True, category=category)
        return render(request, "auctions/index.html", {
            "listings": l,
            "category": Category.objects.all()
        })
