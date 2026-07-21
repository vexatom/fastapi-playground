from itertools import count

import pytest
from starlette.testclient import TestClient

from src.task_manager import main
from src.task_manager import storage


@pytest.fixture
def client():
    client = TestClient(app=main.app)
    return client


@pytest.fixture(autouse=True)
def clear_tasks():
    storage.tasks.clear()
    storage.task_last_id = count(1)

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
