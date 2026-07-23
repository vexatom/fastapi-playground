from src.task_manager.database import connection
from src.task_manager.schemas import Note, NoteCreate


def _row_to_note(row: tuple):
    return Note(
        id=row[0],
        title=row[1],
        description=row[2]
    )


def get_all_notes() -> list[Note]:
    rows = connection.db.get_all_notes()
    return [_row_to_note(row) for row in rows]


def get_note(note_id: int) -> Note:
    return _row_to_note(connection.db.get_note(note_id))


def add_note(note_create: NoteCreate) -> Note:
    last_id = connection.db.insert_note(note_create)

    return Note(
        id=last_id,
        title=note_create.title,
        description=note_create.description
    )


def delete_note(note_id: int) -> None:
    connection.db.delete_note(note_id)


def update_note(note_id: int, note_create: NoteCreate) -> Note:
    connection.db.update_note(note_id, note_create)
    return _row_to_note(connection.db.get_note(note_id))
