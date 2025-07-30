







import os
import sys
from rq import Worker, Queue
from redis import Redis
import redis

# Try to use a real Redis server, fall back to fakeredis for testing
try:
    # Настройка подключения Redis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    conn = redis.from_url(redis_url)
    # Test the connection
    conn.ping()
except (redis.ConnectionError, redis.AuthenticationError):
    print("[WARNING] Could not connect to Redis server, using fakeredis for testing")
    from fakeredis import FakeStrictRedis
    conn = FakeStrictRedis()

listen = ['default']

if __name__ == '__main__':
    queues = [Queue(name, connection=conn) for name in listen]
    worker = Worker(queues)
    worker.work()






