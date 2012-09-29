from django.conf import settings as django_settings


DEFAULT_EXPIRE_TIME = getattr(django_settings, 'GENERIC_CONFIRMATION_DEFAULT_EXPIRE_TIME', 86400)