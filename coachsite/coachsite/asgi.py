import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coachsite.settings")

application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Coach_Site.routing  # Ensure this is Coach_Site, not CoachSite

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": AuthMiddlewareStack(
            URLRouter(Coach_Site.routing.websocket_urlpatterns)
        ),
    }
)
print(os.environ.get("DJANGO_SETTINGS_MODULE"))
