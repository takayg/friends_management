"""
WSGI config for friends_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friends_management.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friends_management.settings.base')

application = get_wsgi_application()
