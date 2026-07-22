from typing import Optional

from fastapi import APIRouter

from src.task_manager.schemas import TaskCreate
from src.task_manager.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get('/')
def get_tasks(priority: Optional[int] = None):
    tasks = task_service.get_tasks(priority)
    return {'tasks': tasks}


@router.get('/{task_id}')
def get_task(task_id: int):
    task = task_service.get_task(task_id)
    return {'task': task}


@router.post('/')
def add_task(task_create: TaskCreate):
    task = task_service.create_task(task_create)
    return {'message': 'Task added', 'task': task}


@router.put('/{task_id}')
def update_task(task_id: int, task_create: TaskCreate):
    task = task_service.update_task(task_id, task_create)
    return {'message': 'Task updated', 'task': task}


@router.delete('/{task_id}')
def delete_task(task_id: int):
    task = task_service.delete_task(task_id)
    return {'message': 'Task deleted', 'task': task}
