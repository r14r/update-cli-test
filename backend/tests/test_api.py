from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "update-cli-test"}


def test_message():
    assert client.get("/api/message").json() == {"message": "Hello from FastAPI"}


def test_add():
    assert client.post("/api/add", json={"a": 20, "b": 22}).json() == {"result": 42}
