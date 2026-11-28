from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models
import schemas
from jose import jwt
from helper import create_token
from pwdlib import PasswordHash
import os 
from dotenv import load_dotenv
from datetime import datetime, timezone
import time

load_dotenv()

Base.metadata.create_all(engine)

app = FastAPI()

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_pass, hash_pass):
    return password_hash.verify(plain_pass, hash_pass)


def verify_token(token: str = Header(None)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token!")


@app.get("/")
def home():
    return {"message" : "Home"}

@app.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blog(blog_data: schemas.BlogBase, db: Session = Depends(get_db), payload = Depends(verify_token)):
    currrent_user = db.query(models.Users).filter(models.Users.username == payload["sub"]).first()
    if currrent_user is None:
        raise HTTPException(status_code=404, detail="user not found!")
    
    data = models.BlogData(
        author=currrent_user.username,
        title=blog_data.title,
        content=blog_data.content,
        user_id = currrent_user.id
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@app.get("/blogs", response_model=list[schemas.BlogOut])
def get_blogs(db: Session = Depends(get_db), payload = Depends(verify_token)):
    blogs = db.query(models.BlogData).all()
    return blogs


@app.get("/blogs/{blog_id}", response_model=schemas.BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db), payload = Depends(verify_token)):
    blog = db.query(models.BlogData).filter(models.BlogData.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found!")

    return blog


@app.put("/blogs/{blog_id}")
def update_blog(blog_id: int, blog_data: schemas.BlogBase, db: Session = Depends(get_db), payload = Depends(verify_token)):
    blog = db.query(models.BlogData).filter(models.BlogData.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404,detail="Blog not found!")

    current_user = db.query(models.Users).filter(models.Users.username == payload["sub"]).first()
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own blogs")
    
    blog.title = blog_data.title
    blog.content = blog_data.content

    db.commit()
    db.refresh(blog)

    return{
        "message" : "blog updated",
        "blog" : blog
    }

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db :  Session = Depends(get_db), payload = Depends(verify_token)):
    blog = db.query(models.BlogData).filter(models.BlogData.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found!")

    current_user = db.query(models.Users).filter(models.Users.username == payload["sub"]).first()
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own blogs")
    
    db.delete(blog)
    db.commit()
    return{
        "message" : "Blog deleted!"
    }

@app.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def register_user(user_data : schemas.UserIn, db : Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username==user_data.username).first()
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists!")

    user_email = db.query(models.Users).filter(models.Users.email==user_data.email).first()

    if user_email is not None:
        raise HTTPException(status_code=400, detail="Email already exists!")

    hash_pass = get_password_hash(user_data.password)

    new_user = models.Users(username = user_data.username,
                            email = user_data.email,
                            hashed_password = hash_pass
                            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login_user(body: schemas.userLoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username== body.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="username is not correct!")

    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password is not correct!")

    token = create_token({
        "sub" : body.username
    })
    return token

