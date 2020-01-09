from django.conf.urls import url
from django.urls import path
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

from Home.consumers import EchoConsumer
application = ProtocolTypeRouter({
    
    
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("profileaccount/", EchoConsumer),
          
        ])
    ),
    # Empty for now (http->django views is added by default)
})