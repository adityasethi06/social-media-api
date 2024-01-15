from .config import base_config
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# commenting below as alembic is handeling table creation
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)