from fastapi import BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from app.core import config
from fastapi import APIRouter, Depends

from app.worker import celery, create_task

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
def run_task():
    task = create_task.delay()
    return JSONResponse({"task_id": task.id})


@router.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
