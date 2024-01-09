from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..utils import validate_login_pwd
from ..oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=login_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Please login with correct email or password")
    user_hashed_pwd = user.password
    if not validate_login_pwd(login_data.password, user_hashed_pwd):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Please login with correct email or password")
    
    access_token = create_access_token({"id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


