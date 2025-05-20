from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.auth import get_db, get_current_user

router = APIRouter(
    prefix="/readers",
    tags=["readers"]
)

@router.post("/", response_model=schemas.ReaderOut)
def create(reader: schemas.ReaderCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.create_reader(db, reader)

@router.get("/", response_model=list[schemas.ReaderOut])
def get_all(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.get_readers(db)

@router.get("/{reader_id}", response_model=schemas.ReaderOut)
def get_one(reader_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.get_reader(db, reader_id)

@router.put("/{reader_id}", response_model=schemas.ReaderOut)
def update(reader_id: int, reader: schemas.ReaderCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.update_reader(db, reader_id, reader)

@router.delete("/{reader_id}", response_model=schemas.ReaderOut)
def delete(reader_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.delete_reader(db, reader_id)