from fastapi import HTTPException

from src.task_manager.repositories import note_repository
from src.task_manager.schemas import NoteCreate, Note


def get_notes() -> list[Note]:
    return note_repository.get_all_notes()


def get_note(note_id: int) -> Note:
    note = note_repository.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


def create_note(note_create: NoteCreate) -> Note:
    return note_repository.add_note(note_create)


def delete_note(note_id: int) -> Note:
    note = get_note(note_id)
    note_repository.delete_note(note_id)
    return note


def update_note(note_id: int, note_create: NoteCreate) -> Note:
    return note_repository.update_note(note_id, note_create)
