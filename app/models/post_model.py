from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str #айдишка
    title: str   #название
    content: str #основной текст
    created_at: datetime = Field(default_factory=datetime.utcnow) #время

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True