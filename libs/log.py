from django.conf import settings
import logging

class RequireDebugFalse(logging.Filter):
    def filter(self, record):
        return not settings.DEBUG