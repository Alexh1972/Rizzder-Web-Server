from django.urls import path, include
from .messaging import ChatConsumer

websocket_urlpatterns = [
    path("wss/<str:room_name>/", ChatConsumer.as_asgi()),
]
