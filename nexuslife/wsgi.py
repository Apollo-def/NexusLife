"""
WSGI config for nexuslife project.

It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Este arquivo configura a integração com servidores web compatíveis com WSGI (Web Server Gateway Interface).
# É o ponto de entrada para a sua aplicação quando executada em um ambiente de produção síncrono.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexuslife.settings')

application = get_wsgi_application()
