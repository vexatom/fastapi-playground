from fastapi import APIRouter

from src.task_manager.schemas import Note, NoteCreate
from src.task_manager.services import note_service

router = APIRouter(prefix='/notes', tags=['notes'])


@router.get('/')
def get_notes():
    notes = note_service.get_notes()
    return {'notes': notes}


@router.get('/{note_id}')
def get_note(note_id: int):
    note = note_service.get_note(note_id)
    return {'note': note}


@router.post('/')
def add_note(note_create: NoteCreate):
    note = note_service.create_note(note_create)
    return {'message': 'Note added', 'note': note}


@router.delete('/{note_id}')
def delete_note(note_id: int):
    note = note_service.delete_note(note_id)
    return {'message': 'Note deleted', 'note': note}


@router.put('/{note_id}')
def update_note(note_id: int, note_create: NoteCreate):
    note = note_service.update_note(note_id, note_create)
    return {'message': 'Note updated', 'note': note}
