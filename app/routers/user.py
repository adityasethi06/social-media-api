from fastapi import status, Depends, HTTPException , APIRouter
from ..schemas import UserCreateResponse, UserInfo, UserCreate
from ..models import User
from ..database import get_db
from sqlalchemy.orm import Session
from app.utils import hash_pwd
from ..oauth2 import get_current_user

router = APIRouter(prefix='/users', tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def create_user(user: UserCreate,  db: Session = Depends(get_db)):
    hashed_pwd = hash_pwd(user.password)
    user.password = hashed_pwd
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserInfo)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter_by(id=id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")
    return user