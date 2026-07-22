from starlette.testclient import TestClient


def test_get_task_raises_404_http_error(client: TestClient) -> None:
    response = client.get("/tasks/-1")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}


def test_add_task_correctly_adds_task(client: TestClient) -> None:
    task_name = "Test Task"
    task_description = "Test Description"
    task_priority = 2

    post_response = client.post("/tasks",json={
        "title": task_name,
        "description": task_description,
        "priority": task_priority
    })

    assert post_response.status_code == 200

    task_id = post_response.json()['task']['id']
    answer = {
        "task": {
            "id": task_id,
            "title": task_name,
            "description": task_description,
            "priority": task_priority
        }
    }

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json() == answer

def test_update_task_correctly_updates_task(client: TestClient, old_task, new_task) -> None:
    post_response = client.post("/tasks",json=old_task)

    assert post_response.status_code == 200

    task_id = post_response.json()['task']['id']
    answer = new_task.copy()
    answer["id"] = task_id

    put_response = client.put(f"/tasks/{task_id}",json=new_task)

    assert put_response.status_code == 200
    assert put_response.json()['task'] == answer

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()['task'] == answer

def test_crud_task_correctly_works(client: TestClient, old_task, new_task) -> None:
    post_response = client.post("/tasks",json=old_task) # Creating task

    assert post_response.status_code == 200

    task_id = post_response.json()['task']['id'] # Extracting task ID

    old_task_answer = old_task.copy()
    old_task_answer['id'] = task_id

    response = client.get(f"/tasks/{task_id}")  # Getting updated task

    assert response.status_code == 200
    assert response.json()['task'] == old_task_answer # Checking added task

    put_response = client.put(f"/tasks/{task_id}",json=new_task) # Updating added task

    new_task_answer = new_task.copy()
    new_task_answer['id'] = task_id

    assert put_response.status_code == 200
    assert put_response.json()['task'] == new_task_answer

    response = client.get(f"/tasks/{task_id}") # Getting updated task

    assert response.status_code == 200
    assert response.json()['task'] == new_task_answer # Checking updated task

    delete_response = client.delete(f"/tasks/{task_id}") # Deleting the task

    assert delete_response.status_code == 200
    assert delete_response.json()['task'] == new_task_answer

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'} # Checking whether delete the task

