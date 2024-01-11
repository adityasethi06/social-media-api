from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# pydantic model, structure for incoming HTTP requests/resposne
# fastapi used this model to inetrnally validates incoming req.
# if it does not follow this strcuture, then fastapi returns bad req error
# this way client cannot pass whatever they want to pass in HTTP req


# pydantic models for incoming HTTP requests
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Login(BaseModel):
    email: EmailStr
    password: str

# pydantic models for HTTP response

class UserInfo(BaseModel):
    id: int
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserCreateResponse(UserInfo):
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    expiry: int

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserCreateResponse

