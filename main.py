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

@app.post("/create-blog")
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


@app.get("/blogs", response_model=list[schemas.BlogOut])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.BlogData).all()
    return blogs


@app.get("/blogs/{blog_id}", response_model=schemas.BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.BlogData).filter(models.BlogData.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found!")

    return blog


@app.put("/update-blog/{blog_id}")
def update_blog(blog_id: int, blog_data: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.BlogData).filter(models.BlogData.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404,detail="Blog not found!")
    print(blog.id, blog.title, blog.author, blog.content)
    blog.author = blog_data.author
    blog.title = blog_data.title
    blog.content = blog_data.content

    db.commit()
    db.refresh(blog)

    return{
        "message" : "blog updated",
        "blog" : blog
    }

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db :  Session = Depends(get_db)):
    blog = db.query(models.BlogData).filter(models.BlogData.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found!")

    db.delete(blog)
    db.commit()
    return{
        "message" : "Blog deleted!"
    }