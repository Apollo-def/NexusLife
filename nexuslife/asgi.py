"""
ASGI config for nexuslife project.

It exposes the ASGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Este arquivo configura a integração com servidores web compatíveis com ASGI (Asynchronous Server Gateway Interface).
# É usado para habilitar funcionalidades assíncronas, como WebSockets.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexuslife.settings')

application = get_asgi_application()
