from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message" : "Home"}