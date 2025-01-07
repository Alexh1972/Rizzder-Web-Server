from ..models import User
from django.shortcuts import render, HttpResponse, redirect
from ..utils import JWTTokenDecoder
import logging

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")
