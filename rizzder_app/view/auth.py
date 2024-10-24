from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.views import APIView
from ..serializer import user_registration_serializer
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def signup(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        ### TODO add all user's data and save it
        return redirect('login')
    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    return render(request, 'registration/login.html')


class user_registration(APIView):
    def post(self, request):
        serializer = user_registration_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'user': user.username, 'data': 'Registration successful'})
        return Response(serializer.errors)

