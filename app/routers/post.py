from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schemas import PostBase, PostCreate, PostResponse
from ..database import get_db
from ..models import Post
from ..oauth2 import get_current_user

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), logged_user_id: int = Depends(get_current_user)):
    # using sqlalchemy orm
    new_post = Post(title=post.title, content=post.content, published=post.published, user_id=logged_user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db), logged_user_id: int = Depends(get_current_user)): # by adding type int, fastapi will take care of typcasting path param to int or throw error
    post = db.query(Post).filter_by(id=id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No post found with id: {id}")
    
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db), logged_user_id: int = Depends(get_current_user)):
    deleted_post = db.query(Post).filter_by(id=id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not there")
    db.delete(deleted_post)
    db.commit()
    return f"post with id: {id} deleted"

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostBase, respone: Response, db: Session = Depends(get_db), logged_user_id: int = Depends(get_current_user)):
    update_post_candidate = db.query(Post).filter_by(id=id).first()
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
