from asyncio import sleep
from celery import Celery

# import debugpy
# debugpy.listen(('0.0.0.0', 5680))

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

@celery.task
def dummy_task():
    sleep(10)
    return {"status": "success"}
