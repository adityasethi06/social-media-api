from pydantic import BaseModel
from datetime import datetime

# pydantic model, structure for incoming HTTP requests/resposne
# fastapi used this model to inetrnally validates incoming req.
# if it does not follow this strcuture, then fastapi returns bad req error
# this way client cannot pass whatever they want to pass in HTTP req


# pydantic models for HTTP requests
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# pydantic models for HTTP response

class PostResponse(PostBase):
    id: int
    created_at: datetime