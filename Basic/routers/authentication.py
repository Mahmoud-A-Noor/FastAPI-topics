from fastapi import APIRouter, Depends, status,  HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from JWT_Token import create_access_token
import models
from database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext



router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto") ### this is used to hash the password ###
    hashed_password = pwd_ctx.hash(request.password)
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not pwd_ctx.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

