from fastapi import FastAPI
from .database import engine, get_db
from . import models
from typing import List
from .utils import hash_pwd
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)