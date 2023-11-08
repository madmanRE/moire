from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import Profile
from .forms import RegisterForm
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.db import IntegrityError


class RegisterView(View):
    def get(self, request):
        form = RegisterForm
        return render(request, "register_app/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = User.objects.create_user(username=username)
                user.set_password(password)
                user.save()
                login(request, user)
                profile = Profile.objects.create(
                    user=user,
                    username=username,
                    password=password,
                    phone=form.cleaned_data["phone"],
                    email=form.cleaned_data["email"],
                )
                profile.save()
                return redirect("/")
            except IntegrityError:
                form.add_error("login", "Пользователь с таким логином уже существует")

        return render(request, "register_app/register.html", {"form": form})
