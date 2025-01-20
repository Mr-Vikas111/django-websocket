from django.urls import path
from . import consumers


websocket_urls = [
    # path("ws/sc/<str:groupname>/",consumers.MySyncConsumer.as_asgi()),
    # path("ws/ac/<str:groupname>/",consumers.MyAsyncConsumer.as_asgi()),
    path("ws/wsc/<str:groupname>/",consumers.MySyncWebsocketConsumer.as_asgi()),
    path("ws/asc/<str:groupname>/",consumers.MyAsyncWebsocketConsumer.as_asgi()),
]