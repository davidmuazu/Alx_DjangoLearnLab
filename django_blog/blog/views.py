from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileForm

# Create your views here.


def home(request):
    return render(request, "blog/base.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. You are now logged in.")
            login(request, user)  # auto-login after register (optional)
            return redirect("profile")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "registration/profile.html", {"form": form})

