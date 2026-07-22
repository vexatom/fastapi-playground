from starlette.testclient import TestClient


def test_get_root_returns_greeting_message(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World!'}

