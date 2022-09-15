from typing import List
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None



class ShowBlog(Blog): ### we extended the blog since we want all fields of Blog ###
    class Config():
        orm_mode = True


### use this in case you want to get specific fields ###

# class ShowBlog(BaseModel):
#     title: str

#     class Config():
#         orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class ShowBlogWithUser(ShowBlog):
    creator: ShowUser

    class Config():
        orm_mode = True

class ShowUserWithBlogs(ShowUser):
    blogs: List[ShowBlog] = []

    class Config():
        orm_mode = True