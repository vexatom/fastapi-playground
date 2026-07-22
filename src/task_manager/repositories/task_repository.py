from src.task_manager import storage
from src.task_manager.schemas import Task


def add_task(task: Task) -> None:
    storage.tasks.append(task)


def delete_task(task: Task) -> None:
    storage.tasks.remove(task)


def get_list_tasks() -> list[Task]:
    return storage.tasks.copy()


def get_task(task_id: int) -> Task | None:
    for task in storage.tasks:
        if task.id == task_id:
            return task
    return None
