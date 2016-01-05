"""
WSGI config for vendor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import socket

env = socket.gethostname()

from django.core.wsgi import get_wsgi_application

settings_file = "vendor.settings_" + env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)

application = get_wsgi_application()
