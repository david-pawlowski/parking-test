"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = (
    "app.production" if os.environ.get("IS_PROD") else "app.settings"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_wsgi_application()

if not os.environ.get("IS_PROD"):
    import debugpy

    debugpy.listen(("0.0.0.0", 5678))
