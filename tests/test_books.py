import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    email = f"bookadmin_{uuid.uuid4()}@example.com"
    password = "securepass123"

    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post(
    "/auth/login",
    data={"username": email, "password": password},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

    assert response.status_code == 200, f"Ошибка при логине: {response.text}"
    return response.json()["access_token"]


def test_add_and_get_book():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    isbn = str(uuid.uuid4())[:13]
    response = client.post("/books/", json={
        "title": "1984",
        "author": "Джордж Оруэлл",
        "year": 1949,
        "isbn": isbn,
        "copies": 3
    }, headers=headers)
    assert response.status_code == 200, f"Ошибка при добавлении книги: {response.text}"
    book_id = response.json()["id"]

    response = client.get("/books/", headers=headers)
    assert response.status_code == 200
    books = response.json()
    assert any(book["id"] == book_id for book in books), "Добавленная книга не найдена в списке"


def test_access_books_without_token():
    response = client.get("/books/")
    assert response.status_code == 401