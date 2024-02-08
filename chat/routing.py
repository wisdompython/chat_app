from django.urls import re_path
from .consumers import ChatConsumer, PrivateMessage
# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)$', ChatConsumer.as_asgi())
# ]

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/private/((?P<room_name>\w+)/$',PrivateMessage.as_asgi())
]