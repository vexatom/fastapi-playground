from src.task_manager.database import sqlite_storage
from src.task_manager.schemas import Task, TaskCreate

db = sqlite_storage.SQLiteDatabase('data.db')


def _row_to_task(row) -> Task:
    return Task(
        id=row[0],
        title=row[1],
        description=row[2],
        priority=row[3]
    )


def add_task(task_create: TaskCreate) -> None:
    last_id = db.insert_task(task_create)

    return Task(
        id=last_id,
        title=task_create.title,
        description=task_create.description,
        priority=task_create.priority
    )


def delete_task(task_id: int) -> None:
    db.delete_task(task_id)


def get_all_tasks() -> list[Task]:
    rows = db.get_all_tasks()

    return [_row_to_task(row) for row in rows]


def get_task(task_id: int) -> Task | None:
    row = db.get_task(task_id)
    if row:
        return _row_to_task(row)
    return None


def get_priority_tasks(priority: int) -> list[Task]:
    rows = db.get_priority_tasks(priority)
    return [_row_to_task(row) for row in rows]


def update_task(task_id: int, task_create: TaskCreate) -> Task:
    db.update_task(task_id, task_create)
    return _row_to_task(db.get_task(task_id))
