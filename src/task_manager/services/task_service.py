from fastapi import HTTPException
from src.task_manager.schemas import TaskCreate, Task
from src.task_manager.repositories import task_repository


def get_task(task_id: int) -> Task:
    task = task_repository.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def create_task(task_create: TaskCreate) -> Task:
    return task_repository.add_task(task_create)


def get_tasks(priority: int | None) -> list[Task]:
    if priority is None:
        return task_repository.get_all_tasks()
    return task_repository.get_priority_tasks(priority)


def update_task(task_id: int, task_create: TaskCreate) -> Task:
    return task_repository.update_task(task_id, task_create)


def delete_task(task_id: int) -> Task:
    task = get_task(task_id)
    task_repository.delete_task(task_id)
    return task
