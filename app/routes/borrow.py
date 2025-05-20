from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.auth import get_db, get_current_user

router = APIRouter(
    prefix="/borrow",
    tags=["borrow"]
)

@router.post("/", response_model=schemas.BorrowOut)
def borrow(data: schemas.BorrowCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.create_borrowing(db, data)

@router.post("/return/{borrow_id}", response_model=schemas.BorrowOut)
def return_book(borrow_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.return_book(db, borrow_id)

@router.get("/", response_model=list[schemas.BorrowOut])
def get_all(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.get_all_borrowings(db)