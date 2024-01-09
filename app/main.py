from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .schemas import PostBase, PostCreate, PostResponse, UserCreate, UserCreateResponse, User
from .database import engine, get_db
from . import models
from typing import List
from .utils import hash_pwd


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    # using sqlalchemy orm
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # using regular sql via adapter
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
    #                (post.title, post.content, post.published))
    # inserted_post = cursor.fetchone()
    # conn.commit()
    return new_post

@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)): # by adding type int, fastapi will take care of typcasting path param to int or throw error
    post = db.query(models.Post).filter_by(id=id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No post found with id: {id}")
    
@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter_by(id=id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not there")
    db.delete(deleted_post)
    db.commit()
    return f"post with id: {id} deleted"

@app.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, post: PostBase, respone: Response, db: Session = Depends(get_db)):
    update_post_candidate = db.query(models.Post).filter_by(id=id).first()
    if not update_post_candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not there")    
        
    update_post_data = post.model_dump()
    for key, val in update_post_data.items():
        setattr(update_post_candidate, key, val) if val else None
    db.commit()
    db.refresh(update_post_candidate)
    respone.status_code = status.HTTP_201_CREATED
    return update_post_candidate


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def create_user(user: UserCreate,  db: Session = Depends(get_db)):
    hashed_pwd = hash_pwd(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")
    return user