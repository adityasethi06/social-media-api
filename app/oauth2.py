from jose import JWTError, jwt
from datetime import datetime, timedelta

#SECRET KEY
#Alogrithm
#Expiration time

SECRET_KEY = "RRER67878IRE6767FOIERORERENVCVMSDCSDCSDC4323223234E234KJNFFYT6Y756JNY56908VN0332323292"
ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.now() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    to_encode.update({"exp": expiry})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



