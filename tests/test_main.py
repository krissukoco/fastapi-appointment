from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_ping():
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert data['message'] == 'pong'