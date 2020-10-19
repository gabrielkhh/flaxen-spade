from os import getenv

from flask_caching import Cache

cache = Cache(
    config={
        "CACHE_TYPE": getenv("CACHE_TYPE", "simple"),
        "CACHE_REDIS_URL": getenv("REDIS_URL", "redis://localhost:6379/0"),
        "CACHE_REDIS_PASSWORD": getenv("REDIS_PASSWORD"),
        "CACHE_KEY_PREFIX": "flaxen-spade",
    }
)
