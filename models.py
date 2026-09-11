from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime, timezone


class BlogData(Base):
    __tablename__ = "blog_data"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    title = Column(String)
    content = Column(String)
    date_published = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
