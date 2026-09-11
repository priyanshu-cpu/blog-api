from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models
import schemas

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message" : "Home"}

@app.post("/create")
def create_blog(blog_data: schemas.BlogBase, db: Session = Depends(get_db)):
    data = models.BlogData(
        author=blog_data.author,
        title=blog_data.title,
        content=blog_data.content
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data