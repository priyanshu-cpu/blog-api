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

@app.post("/create", response_model=schemas.BlogOut)
def create_blog(db: Session= Depends(get_db)):
    pass