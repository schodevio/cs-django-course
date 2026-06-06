from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm


@require_GET
def new(request):
    form = UserRegisterForm()
    return render(request, "users/new.html", {"form": form})


@require_POST
def create(request):
    form = UserRegisterForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Your account has been created!")
        return redirect("login")
    else:
        messages.error(request, "Please correct the error below.")
        return render(request, "users/new.html", {"form": form})


@require_GET
@login_required
def profile(request):
    return render(request, "users/profile.html")
