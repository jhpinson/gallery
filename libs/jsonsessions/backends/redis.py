from redisession.backend import SessionStore as RedisessionSessionStore
from .base import JsonSessionMixin

class SessionStore(JsonSessionMixin, RedisessionSessionStore):
    pass