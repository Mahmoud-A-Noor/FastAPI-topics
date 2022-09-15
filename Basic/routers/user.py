from fastapi import APIRouter
from fastapi import Depends, status
import schemas
from database import get_db
from sqlalchemy.orm import Session
from repository import user


router = APIRouter(
    prefix="/user",
    tags=['Users']
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db=db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUserWithBlogs)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db=db)
