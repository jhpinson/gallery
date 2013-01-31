from os import environ
import common
from cacheutils.manager import manager as cache_manager
from os import environ



# cacheops
"""common.INSTALLED_APPS += (
    'cacheops',    
)

common.CACHEOPS = {
    '*.*': ('all', 60*10)
}

common.CACHEOPS_REDIS = {
    'host':  environ.get('REDIS_HOST', '127.0.0.1') , 
    'port': 6379,        
    'db': 1,                    
    'socket_timeout': 4,
}
"""
cache_manager.register('cacheops', 'redis', {
    'host' : environ.get('REDIS_HOST', '127.0.0.1') ,
    'port': 6379,
    'db': 1
    })


# default cache
common.CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': environ.get('REDIS_HOST', '127.0.0.1') + ':6379',
        'OPTIONS': {
            'DB': 2,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        }
    }
}

cache_manager.register('default', 'redis', {
    'host' :  environ.get('REDIS_HOST', '127.0.0.1') ,
    'port': 6379,
    'db': 2
    })

# Thumbnail
common.THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
common.THUMBNAIL_REDIS_DB = 3

cache_manager.register('thumbnail', 'redis', {
    'host' :  environ.get('REDIS_HOST', '127.0.0.1') ,
    'port': 6379,
    'db': 3
    })


# sessions
common.REDIS_SESSION_CONFIG = {
    'SERVER': {'port':6379, 'db':4, 'host' :  environ.get('REDIS_HOST', '127.0.0.1') },
    'USE_HASH': True,
    'KEY_GENERATOR': lambda x: x.decode('hex'),
    'HASH_KEY_GENERATOR': lambda x: x[:4].decode('hex'),
    'HASH_KEYS_CHECK_FOR_EXPIRY': lambda r: (reduce(lambda p,y :p.randomkey(),
        xrange(100), r.pipeline()).execute()),
    'COMPRESS_LIB': None,
    'COMPRESS_MIN_LENGTH': 400,
    'LOG_KEY_ERROR': False
}

cache_manager.register('sessions', 'redis', {
    'host' :  environ.get('REDIS_HOST', '127.0.0.1') ,
    'port': 6379,
    'db': 4
    })

#common.SESSION_ENGINE='jsonsessions.backends.redis'
common.SESSION_ENGINE='redisession.backend'