from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    user_id: str
    title: str
    content: str

class PostResponse(BaseModel):
    id: str | None = None
    user_id: str
    title: str
    content: str
    created_at: datetime