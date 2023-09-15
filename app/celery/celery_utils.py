from celery import current_app as current_celery_app

from settings import settings

from redis import Redis
from redis.lock import Lock as RedisLock


def creat_redis_lock():
    redis_instance = Redis.from_url(settings.REDIS_URL)
    lock = RedisLock(redis_instance, name="task_id")
    return [lock, redis_instance]


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")
    return celery_app
