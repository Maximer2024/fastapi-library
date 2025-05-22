from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas
from app.auth import create_user, get_db, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = authenticate_user(form_data.username, form_data.password, db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}