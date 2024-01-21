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

API_PREFIX = '/api/v1'
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(post.router, prefix=API_PREFIX)
app.include_router(user.router, prefix=API_PREFIX)
app.include_router(vote.router, prefix=API_PREFIX)