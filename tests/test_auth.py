import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    unique_email = f"testuser_{uuid.uuid4()}@example.com"
    password = "StrongPassword123"

    response = client.post("/auth/register", json={
        "email": unique_email,
        "password": password
    })
    assert response.status_code == 200, f"Ошибка регистрации: {response.text}"
    data = response.json()
    assert "id" in data
    assert data["email"] == unique_email

    response = client.post("/auth/login", data={
        "username": unique_email,
        "password": password
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200, f"Ошибка логина: {response.text}"

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_protected_route_requires_token():
    response = client.get("/books/")
    assert response.status_code == 401