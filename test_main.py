from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/user", json={"email": "user_email@gmail.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json() == {"email": "user_email@gmail.com"}

def test_create_tournament():
    response = client.post("/tournament", json={"name": "Test Tournament"})
    assert response.status_code == 201
    assert response.json() == {"name": "Test Tournament"}
