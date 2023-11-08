from django import forms
from .models import Profile
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = Profile
        fields = ("username", "phone", "email")
