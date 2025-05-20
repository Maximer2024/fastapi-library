from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.auth import get_db, get_current_user

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/", response_model=schemas.BookOut)
def create(book: schemas.BookCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.create_book(db, book)

@router.get("/", response_model=list[schemas.BookOut])
def get_all(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.get_books(db)

@router.get("/{book_id}", response_model=schemas.BookOut)
def get_one(book_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.get_book(db, book_id)

@router.put("/{book_id}", response_model=schemas.BookOut)
def update(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.update_book(db, book_id, book)

@router.delete("/{book_id}", response_model=schemas.BookOut)
def delete(book_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.delete_book(db, book_id)