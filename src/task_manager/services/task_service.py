from fastapi import HTTPException
from src.task_manager.schemas import TaskCreate, Task
from src.task_manager.repositories import task_repository
from src.task_manager import storage


def get_task(task_id: int) -> Task:
    task = task_repository.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def create_task(task_create: TaskCreate) -> Task:
    task = Task(
        id=next(storage.task_last_id),
        title=task_create.title,
        description=task_create.description,
        priority=task_create.priority
    )
    task_repository.add_task(task)
    return task


def get_tasks(priority: int | None) -> list[Task]:
    tasks = task_repository.get_list_tasks()
    if priority is None:
        return tasks
    else:
        priority_tasks = [task for task in tasks if task.priority == priority]
        return priority_tasks


def update_task(task_id: int, task_create: TaskCreate) -> Task:
    task = get_task(task_id)
    task.title = task_create.title
    task.description = task_create.description
    task.priority = task_create.priority
    return task


def delete_task(task_id: int) -> Task:
    task = get_task(task_id)
    task_repository.delete_task(task)
    return task
