"""
ASGI config for realtimetracking project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtimetracking.settings')


application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from pizzatracker.consumer import OrderProgess



ws_pattern = [
    path("ws/pizza/<order_id>/",OrderProgess),
]

application = ProtocolTypeRouter({
    "websocket": (
        (
            URLRouter(ws_pattern)
        )
    ),
})
