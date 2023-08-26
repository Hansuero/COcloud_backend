# chat/routing.py
from django.template.defaulttags import url
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<room_name>", consumers.ChatConsumer.as_asgi()),
]