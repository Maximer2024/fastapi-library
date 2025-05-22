from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: Optional[int] = 1

class BookOut(BookCreate):
    id: int

    class Config:
        from_attributes = True

class ReaderCreate(BaseModel):
    full_name: str
    email: EmailStr

class ReaderOut(ReaderCreate):
    id: int
    registered_at: datetime

    class Config:
        from_attributes = True

class BorrowCreate(BaseModel):
    reader_id: int
    book_id: int

class BorrowOut(BaseModel):
    id: int
    reader_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True