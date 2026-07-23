import pytest
from starlette.testclient import TestClient

from src.task_manager import main


@pytest.fixture
def client():
    client = TestClient(app=main.app)
    return client


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
