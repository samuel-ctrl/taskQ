from asyncio import sleep
from fastapi import BackgroundTasks, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing_extensions import Annotated
from app.core import config
from fastapi import APIRouter, Depends

from app.db.modals import TaskOut
from app.dependencies import get_token_header
from app.tasks.celery_worker import celery, dummy_task
from app.utils import _to_task_out

router = APIRouter(
    prefix="/api",
    tags=["Back Tasks"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

def short_running_task():
    pass

@router.get("/fastApi_background_task")
def background_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(short_running_task)
    return JSONResponse("FastApi task added.")

@router.get("/get_settings")
def fetch_settings(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    return JSONResponse({"app_name": settings.app_name })

@router.post("/tasks", status_code=201)
def celery_task()-> TaskOut:
    res = dummy_task.delay()
    return TaskOut(id=res.task_id, status=res.status)

@router.get("/tasks", status_code=200)
def get_status(task_id:str)->TaskOut:
    res = celery.AsyncResult(task_id)
    return _to_task_out(res)
