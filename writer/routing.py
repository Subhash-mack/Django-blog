from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from users.consumers import EchoConsumer,ChatConsumer
from channels.auth import AuthMiddlewareStack

application=ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
        path('ws/chats/<str:username>/',ChatConsumer.as_asgi()),
        path('ws/chat/',EchoConsumer.as_asgi())
    ])
    )
})