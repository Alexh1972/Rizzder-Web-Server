from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


def login_view(request):
    """ Handle login with username and password (session-based). """
    print("login_view")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        logger.info(f"User {username} is attempting to log in.")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        print(password)

        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            logger.info(f"User {username} logged in successfully.")
            return redirect('home')  # Redir
