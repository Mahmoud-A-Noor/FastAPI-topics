from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from JWT_Token import verify_token


oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oath2_scheme)):
    return verify_token(token)
