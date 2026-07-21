from pydantic import BaseModel


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

