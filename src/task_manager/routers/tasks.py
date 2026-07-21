from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.task_manager import storage

router = APIRouter(prefix="/tasks", tags=["tasks"])


class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: int

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int


def _get_task(task_id: int) -> Task:
    for task in storage.tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.get('/')
def get_tasks(priority: Optional[int] = None):
    if priority is None:
        return {'tasks': storage.tasks}
    else:
        priority_tasks = [task for task in storage.tasks if task.priority == priority]
        return {'tasks': priority_tasks}


@router.get('/{task_id}')
def get_task(task_id: int):
    task = _get_task(task_id)
    return {'task': task}


@router.post('/')
def add_task(task_create: TaskCreate):
    task_id = next(storage.task_last_id)
    task = Task(id=task_id, title=task_create.title, description=task_create.description, priority=task_create.priority)
    storage.tasks.append(task)
    return {'message': 'Task added', 'task': task}


@router.put('/{task_id}')
def update_task(task_id: int, task_create: TaskCreate):
    task = _get_task(task_id)
    task.title = task_create.title
    task.description = task_create.description
    task.priority = task_create.priority
    return {'message': 'Task updated', 'task': task}


@router.delete('/{task_id}')
def delete_task(task_id: int):
    task = _get_task(task_id)
    storage.tasks.remove(task)
    return {'message': 'Task deleted', 'task': task}


