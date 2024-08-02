import os
import time

from celery import Celery
from celery.contrib import rdb

celery = Celery(
    "task",
    broker_url="redis://redis:6379/0",
    result_backend="redis://redis:6379/0",
    broker_connection_retry_on_startup=True,
)


@celery.task(name="create_task")
def create_task():
    print("Task started")
    time.sleep(5)
    print("Task completed")
    return True
