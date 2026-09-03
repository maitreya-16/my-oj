import os
import redis
from celery import Celery
from celery.signals import worker_process_init

redis_client = None

@worker_process_init.connect
def init_worker(**kwargs):
    """
    Triggered once when each individual worker child process spawns.
    Ensures connection pools are decoupled from the parent process.
    """
    global redis_client
    print(f"Initializing Redis pool for Worker Process PID: {os.getpid()}")
    pool = redis.ConnectionPool(
        host=os.getenv('REDIS_HOST', 'redis'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=1,
        decode_responses=True,
        max_connections=10,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
        health_check_interval=30,
    )
    redis_client = redis.Redis(connection_pool=pool)

def get_redis():
    return redis_client