import time
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger("celery_tasks")


@shared_task(bind=True, queue="high_priority")
def fast_dummy_task(self, x):
    logger.info("starting fast background task")
    time.sleep(5)
    return x


@shared_task(bind=True, queue="low_priority")
def slow_dummy_task(self, x):
    logger.info("starting slow background task")
    time.sleep(x)
    return x


@shared_task(name="dummy_periodic_task")
def dummy_periodic_task():
    print("Periodic task in periodic worker")

