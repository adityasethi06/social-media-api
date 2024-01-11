from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schemas import VoteData
from ..database import get_db
from ..models import Vote, Post
from ..oauth2 import get_current_user

router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def get_posts(vote_data: VoteData, db: Session = Depends(get_db), logged_user_id: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id==vote_data.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post: {vote_data.post_id} not found")
    vote = db.query(Vote).filter(Vote.user_id==logged_user_id, Vote.post_id==vote_data.post_id).first()
    if not vote_data.vote_dir in [0,1]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"vote_dir can only be 1 or 0. 1 to vote up and 0 to vote down")
    if vote:
        if vote_data.vote_dir == 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Cannot vote up twice")
        else:
            db.delete(vote)
            db.commit()
            return f"Voted down for post: {vote_data.post_id}"
    else:
        if vote_data.vote_dir == 1:
            new_vote = Vote(post_id=vote_data.post_id, user_id=logged_user_id)
            db.add(new_vote)
            db.commit()
            return f"Voted up for post: {vote_data.post_id}"
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Cannot vote down for unvoted post")