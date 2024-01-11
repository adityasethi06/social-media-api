from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import base_config
import calendar

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET KEY
#Alogrithm
#Expiration time

# secret should never be published to SVC. this is just an app for learning.
SECRET_KEY = base_config.secret_key
ALGORITHM = base_config.jwt_algorithm
ACCESS_TOKEN_DURATION = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    expiry_in_epoch = calendar.timegm(expiry.timetuple())
    to_encode.update({"expiry": expiry_in_epoch})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get('id')
        expiry: int  = payload.get('expiry')
        if id is None:
            raise credentials_exception
        if datetime.fromtimestamp(expiry) < datetime.now():
            raise credentials_exception
        token_data = TokenData(id=id, expiry=expiry)
    except JWTError:
        raise credentials_exception
    return token_data.id
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credential_exception)