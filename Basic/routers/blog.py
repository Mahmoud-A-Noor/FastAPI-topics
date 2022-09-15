from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from oauth import get_current_user
import schemas, models
from database import get_db
from sqlalchemy.orm import Session
from repository import blog


router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)




### get all blogs ###
@router.get("/")
def index(db: Session = Depends(get_db)):
    return blog.get_all_blogs(db=db)


### get all blogs using response model ###
@router.get("/allBlogsResponseModel", response_model=List[schemas.ShowBlog]) ### here we are using a List the response model to specify the response data ###
def index(db: Session = Depends(get_db)):
    return blog.get_all_blogs(db=db)



### since FatAPI check for paths from top to bottom you will get an error if you added a path like  "/blog/unpublished"  after  "/blog/{id}"  ###
### FastAPI will consider "unpublished" as the id but since our id is int you will get a type error response ###



### this route is added just for explanation purpose ###
@router.post("/bloog")
def create_blog(limit = 10, published: bool = True, sort: Optional[str] = None): 
    ### you can ignore putting parameter in the path and pass it in the url as shown => localhost:8000/blog?limit=7 ###
    ### you can also pass multiple values as shown => localhost:8000/blog?limit=7&published=true ###
    ### you must pass all parameters once you specified them in the function ###
    ### you can add optional Parameters which are not required as shown => sort: Optional[DataType] ###
    return {"data": f"Blog is created with {limit} and published is {published} and sort is {sort}"}



### add new blog ###
@router.post("/", status_code=status.HTTP_201_CREATED) ### you can add a default status code to your response like this (it is optional) ###
def create_blog(request: schemas.Blog, userId: int, db: Session = Depends(get_db)):
    return blog.create_blog(request, db=db, userId=userId)



### get blog using response model ###
@router.get("/blogResponseModel/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog) ### here we are using the response model to specify the response data ###
def show(id: int, response: Response, db: Session = Depends(get_db)):
    return blog.get_blog(id, db=db)



### get blog ###
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlogWithUser) ### you can add a default status code to your response like this (it is optional) ###
def show(id: int, response: Response, db: Session = Depends(get_db)): ### specifying the type using :int is like a validation to make sure that data are in the desired type otherwise the passed parameter will be considered as string ###
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog:
        return blog
    else:
        response.status_code = status.HTTP_404_NOT_FOUND ### here we are overWriting the default value of status code ###
        return {"detail": f"Blog with id = {id} not found"}

        ### this is another way to raise an exception ###
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found") 



### update blog ###
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.update_blog(id, request, db)
    


### delete blog ###
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.delete_blog(id, db)