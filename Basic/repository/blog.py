from fastapi import HTTPException, status
import models



def get_all_blogs(db):
    blogs = db.query(models.Blog).all()
    return blogs


def create_blog(request, db):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_blog(id, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found")
    return blog


def update_blog(id, request, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found")
    blog.update(request)
    db.commit()
    return "Blog updated"


def delete_blog(id, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Blog deleted"