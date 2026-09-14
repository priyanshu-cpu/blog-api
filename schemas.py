from pydantic import BaseModel, Field, field_serializer, EmailStr
from datetime import datetime, timezone
from typing import Optional


class BlogBase(BaseModel):
    author: str
    title: str
    content: str

    class Config:
        from_attributes = True


class BlogOut(BaseModel):
    id: int
    author: str
    title: str
    content: str
    date_published : datetime

    @field_serializer("date_published")
    def format_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%B %d, %Y at %I:%M %p")
    
    class Config:
        from_attributes = True


class UserIn(BaseModel):
    username :str
    email: Optional[EmailStr]
    password : str


class UserOut(BaseModel):
    id: int
    username: str
    email: str

class userLoginSchema(BaseModel):
    username: str
    password: str