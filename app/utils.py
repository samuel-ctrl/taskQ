from celery.result import AsyncResult
from app.db.modals import TaskOut

def _to_task_out(r: AsyncResult)->TaskOut:
    return TaskOut(id=r.task_id, status=r.status)
