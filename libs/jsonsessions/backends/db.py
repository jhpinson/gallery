from django.contrib.sessions.backends.db import SessionStore as DbSessionStore
from .base import JsonSessionMixin

class SessionStore(JsonSessionMixin,DbSessionStore):
    pass