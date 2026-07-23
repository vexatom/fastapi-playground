import pytest
from starlette.testclient import TestClient

from src.task_manager import main
from src.task_manager.database import connection
from src.task_manager.database.sqlite_storage import SQLiteDatabase


@pytest.fixture
def client():
    client = TestClient(app=main.app)
    return client


@pytest.fixture(autouse=True)
def connect_database():
    connection.db = SQLiteDatabase('test.db')
    connection.db.clear_tables()


@pytest.fixture
def old_task():
    return {
        "title": "Old Task",
        "description": "Old Description",
        "priority": 0
    }


@pytest.fixture
def new_task():
    return {
        "title": "New Task",
        "description": "New Description",
        "priority": 2
    }
