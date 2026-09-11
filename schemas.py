from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional


class BlogBase(BaseModel):
    author: str
    title: str
    content: str
    date_published : Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

class BlogOut(BaseModel):
    id: int
    author: str
    title: str
    content: str
    date_published : datetime

    class Config:
        from_attributes = True
