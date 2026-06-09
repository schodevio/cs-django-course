from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


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
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)


@require_POST
@login_required
def update_profile(request):
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST,
                               request.FILES,
                               instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, "Your account has been updated!")
        return redirect("users-profile")

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)
