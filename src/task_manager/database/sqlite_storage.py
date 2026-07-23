import sqlite3 as sq

from pathlib import Path

from src.task_manager.schemas import TaskCreate, NoteCreate


class SQLiteDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_path) -> None:
        self.db_path = db_path
        self.prepare()

    def prepare(self) -> None:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT(''),
                priority INTEGER NOT NULL
            )''')

            cur.execute('''CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT('')
            )''')

            conn.commit()

    def clear_tables(self, protection: bool = True) -> None:
        if protection:
            if Path(self.db_path).name != 'test.db':
                raise Exception(f'Are you sure that you want to clear this database ({self.db_path})?')
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM tasks')
            cur.execute('DELETE FROM notes')
            conn.commit()

    def get_all_tasks(self) -> list[tuple]:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM tasks')

            return cur.fetchall()

    def insert_task(self, task_create: TaskCreate) -> int:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute('INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)',
                        (task_create.title, task_create.description, task_create.priority))

            last_id = cur.lastrowid

            conn.commit()

        return last_id

    def delete_task(self, task_id: int) -> None:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

            conn.commit()

    def get_task(self, task_id: int) -> tuple:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            row = cur.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

            return row

    def get_priority_tasks(self, priority) -> list[tuple]:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            rows = cur.execute('SELECT * FROM tasks WHERE priority = ?', (priority,)).fetchall()

        return rows

    def update_task(self, task_id: int, task_create: TaskCreate) -> None:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute('UPDATE tasks SET title = ?, description = ?, priority = ? WHERE id = ?',
                        (task_create.title, task_create.description, task_create.priority, task_id))

            conn.commit()

    def get_all_notes(self) -> list[tuple]:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM notes')

            return cur.fetchall()

    def insert_note(self, note_create: NoteCreate) -> int:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute('INSERT INTO notes (title, description) VALUES (?, ?)',
                        (note_create.title, note_create.description))

            last_id = cur.lastrowid

            conn.commit()

        return last_id

    def delete_note(self, note_id: int) -> None:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute('DELETE FROM note WHERE id = ?', (note_id,))

            conn.commit()

    def get_note(self, note_id: int) -> tuple:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            row = cur.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()

            return row

    def update_note(self, note_id: int, note_create: NoteCreate) -> None:
        with sq.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?',
                        (note_create.title, note_create.description, note_id))

            conn.commit()

