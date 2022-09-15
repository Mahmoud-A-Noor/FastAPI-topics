from fastapi import Depends, status,  HTTPException
import models
from database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext



def create_user(request, db):
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto") ### this is used to hash the password ###
    hashed_password = pwd_ctx.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found")
    return user