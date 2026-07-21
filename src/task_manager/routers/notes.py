from fastapi import APIRouter, HTTPException

from src.task_manager import storage
from src.task_manager.schemas import Note, NoteCreate

router = APIRouter(prefix='/notes', tags=['notes'])


def _get_note(note_id: int) -> Note:
    for note in storage.notes:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@router.get('/')
def get_notes():
    return {'notes': storage.notes}


@router.get('/{note_id}')
def get_note(note_id: int):
    note = _get_note(note_id)
    return {'note': note}


@router.post('/')
def add_note(note_create: NoteCreate):
    note_id = next(storage.note_last_id)
    note = Note(id=note_id, title=note_create.title, description=note_create.description)
    storage.notes.append(note)
    return {'message': 'Note added', 'note': note}


@router.delete('/{note_id}')
def delete_note(note_id: int):
    note = _get_note(note_id)
    storage.notes.remove(note)
    return {'message': 'Note deleted', 'note': note}


@router.put('/{note_id}')
def update_note(note_id: int, note_create: NoteCreate):
    note = _get_note(note_id)
    note.title = note_create.title
    note.description = note_create.description
    return {'message': 'Note updated', 'note': note}

