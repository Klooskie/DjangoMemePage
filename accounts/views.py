from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm


def log_in_view(request):
    form = UserLoginForm(request.POST or None)
    next_page = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        login(request, user)
        if next_page:
            return redirect(next_page)
        return redirect("memes:main")

    context = {
        "form": form,
        "title": "Login",
    }
    return render(request, "accounts/authentication_form.html", context)


def sign_up_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data["password"]
        user.set_password(password)
        user.save()

        log_as_user = authenticate(username=user.username, password=password)
        login(request, log_as_user)
        return redirect("memes:main")

    context = {
        "form": form,
        "title": "Sign up",
    }
    return render(request, "accounts/authentication_form.html", context)


def log_out_view(request):
    logout(request)
    return redirect("memes:main")
