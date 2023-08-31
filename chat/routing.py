
# chat/routing.py
from django.urls import re_path

import chat
import project
from chat import consumers
from project import consumers
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', chat.consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/doc/(?P<doc_id>\w+)/$', project.consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/private/(?P<userid_1>\w+)/(?P<userid_2>\w+)/$', chat.consumers.PrivateChatConsumer.as_asgi()),

]