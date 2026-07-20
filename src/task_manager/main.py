from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from itertools import count

task_last_id = count(1)
note_last_id = count(1)

class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: int

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int

class Note(BaseModel):
    id: int
    title: str
    description: str

class NoteCreate(BaseModel):
    title: str
    description: str

app = FastAPI()

tasks = []
notes = []


def _get_task(task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


def _get_note(note_id: int) -> Note:
    for note in notes:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.get('/')
def root():
    return {'message': 'Hello World!'}


@app.get('/tasks')
def get_tasks(priority: Optional[int] = None):
    if priority is None:
        return {'tasks': tasks}
    else:
        priority_tasks = [task for task in tasks if task.priority == priority]
        return {'tasks': priority_tasks}


@app.get('/tasks/{task_id}')
def get_task(task_id: int):
    task = _get_task(task_id)
    return {'task': task}


@app.post('/tasks')
def add_task(task_create: TaskCreate):
    task_id = next(task_last_id)
    task = Task(id=task_id, title=task_create.title, description=task_create.description, priority=task_create.priority)
    tasks.append(task)
    return {'message': 'Task added', 'task': task}


@app.put('/tasks/{task_id}')
def update_task(task_id: int, task_create: TaskCreate):
    task = _get_task(task_id)
    task.title = task_create.title
    task.description = task_create.description
    task.priority = task_create.priority
    return {'message': 'Task updated', 'task': task}


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    task = _get_task(task_id)
    tasks.remove(task)
    return {'message': 'Task deleted', 'task': task}


@app.get('/notes')
def get_notes():
    return {'notes': notes}


@app.get('/notes/{note_id}')
def get_note(note_id: int):
    note = _get_note(note_id)
    return {'note': note}

@app.post('/notes')
def add_note(note_create: NoteCreate):
    note_id = next(note_last_id)
    note = Note(id=note_id, title=note_create.title, description=note_create.description)
    notes.append(note)
    return {'message': 'Note added', 'note': note}

@app.delete('/notes/{note_id}')
def delete_note(note_id: int):
    note = _get_note(note_id)
    notes.remove(note)
    return {'message': 'Note deleted', 'note': note}

@app.put('/notes/{note_id}')
def update_note(note_id: int, note_create: NoteCreate):
    note = _get_note(note_id)
    note.title = note_create.title
    note.description = note_create.description
    return {'message': 'Note updated', 'note': note}
