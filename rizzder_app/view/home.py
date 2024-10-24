from ..models import *
from django.shortcuts import render, HttpResponse, redirect
def home(request):
    items = User.objects.all()
    return render(request, "home.html", {"test": items})