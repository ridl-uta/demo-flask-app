from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': 'redis://redis:6379/0'})
