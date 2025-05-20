from app import models, schemas
from app.models import Borrowing, Book
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

def get_books(db: Session):
    return db.query(models.Book).all()

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    db.delete(book)
    db.commit()
    return book

def update_book(db: Session, book_id: int, book_data: schemas.BookCreate):
    book = get_book(db, book_id)
    for key, value in book_data.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def create_reader(db: Session, reader: schemas.ReaderCreate):
    db_reader = models.Reader(**reader.dict())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

def get_reader(db: Session, reader_id: int):
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return reader

def get_readers(db: Session):
    return db.query(models.Reader).all()

def update_reader(db: Session, reader_id: int, data: schemas.ReaderCreate):
    reader = get_reader(db, reader_id)
    for key, value in data.dict().items():
        setattr(reader, key, value)
    db.commit()
    db.refresh(reader)
    return reader

def delete_reader(db: Session, reader_id: int):
    reader = get_reader(db, reader_id)
    db.delete(reader)
    db.commit()
    return reader

def create_borrowing(db: Session, data: schemas.BorrowCreate):
    book = db.query(Book).filter(Book.id == data.book_id).first()
    if not book or book.copies < 1:
        raise HTTPException(status_code=400, detail="Книга недоступна")

    book.copies -= 1
    borrow = Borrowing(**data.dict())
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


def return_book(db: Session, borrow_id: int):
    borrow = db.query(Borrowing).filter(Borrowing.id == borrow_id).first()
    if not borrow or borrow.returned_at is not None:
        raise HTTPException(status_code=400, detail="Запись недействительна или уже возвращена")

    borrow.returned_at = datetime.utcnow()

    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    book.copies += 1

    db.commit()
    db.refresh(borrow)
    return borrow


def get_all_borrowings(db: Session):
    return db.query(Borrowing).all()