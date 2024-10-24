from django.shortcuts import render, HttpResponse
from .models import TestEntity

def home(request):
    items = TestEntity.objects.all()
    return render(request, "home.html", {"test": items})
