import redis
from blogproject import settings


def get_redis(**options):
    options = (options or {})

    database = options.get('db', 0)
    max_connections = options.get('max_connections', 100)
    port = options.get('port', settings.REDIS_PORT)
    host = options.get('host', settings.REDIS_HOST)

    r = redis.Redis(host=host,
                    port=port,
                    password=settings.REDIS_PASSWORD,
                    db=database,
                    max_connections=max_connections)

    return r
