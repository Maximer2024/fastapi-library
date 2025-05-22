import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Book, Borrowing, Reader
from datetime import datetime

client = TestClient(app)

def get_token_and_reader_id():
    email = f"reader_{uuid.uuid4()}@example.com"
    password = "readerpass123"

    client.post("/auth/register", json={"email": email, "password": password})
    login_resp = client.post("/auth/login", data={
    "username": email,
    "password": password
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    db = SessionLocal()
    reader = Reader(full_name="Тестовый Читатель", email=f"reader_{uuid.uuid4()}@example.com")
    db.add(reader)
    db.commit()
    db.refresh(reader)
    db.close()

    return token, reader.id

def test_cannot_borrow_unavailable_book():
    db = SessionLocal()
    book = Book(
        title="Нечего брать",
        author="Тест",
        year=2023,
        isbn=str(uuid.uuid4())[:13],
        copies=0
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    db.close()

    token, reader_id = get_token_and_reader_id()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/borrow/", json={
        "book_id": book.id,
        "reader_id": reader_id
    }, headers=headers)

    assert response.status_code == 400
    assert "Книга недоступна" in response.text

def test_cannot_borrow_more_than_3_books():
    token, reader_id = get_token_and_reader_id()
    headers = {"Authorization": f"Bearer {token}"}
    db = SessionLocal()

    isbn = str(uuid.uuid4())[:13]
    book = Book(
        title="Лимитная книга",
        author="Автор",
        year=2022,
        isbn=isbn,
        copies=10
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    for _ in range(3):
        borrowing = Borrowing(reader_id=reader_id, book_id=book.id)
        db.add(borrowing)
        book.copies -= 1
    db.commit()

    response = client.post("/borrow/", json={
        "book_id": book.id,
        "reader_id": reader_id
    }, headers=headers)

    assert response.status_code == 400
    assert "Превышен лимит" in response.text
    db.close()