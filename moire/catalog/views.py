from django.shortcuts import render


def index(request):
    return render(request, "catalog/pages/index.html")
