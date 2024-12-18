from ..models import User
from django.shortcuts import render, HttpResponse, redirect
from ..utils import JWTTokenDecoder
import logging

logger = logging.getLogger(__name__)


def home(request):
    try:
        jwt_token_decoder = JWTTokenDecoder(request)
        user = jwt_token_decoder.getUserFromToken()

        if user == None:
            return redirect("login")

        return render(request, "home.html", {"user": user})
    except Exception as e:
        print(e)
        return redirect("login")
