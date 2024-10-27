from ..models import *
from django.shortcuts import render, HttpResponse, redirect
import logging
from ..utils import *
import json

logger = logging.getLogger(__name__)


def home(request):
    try:
        jwt_token_decoder = JWTTokenDecoder(request.GET['token'])
        user = jwt_token_decoder.getUserFromToken()
        logger.info(user)
        if user == None:
            return redirect("login")

        return render(request, "home.html", {"user": user})
    except:
        return redirect("login")
