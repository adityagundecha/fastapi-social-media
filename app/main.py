from sqlalchemy.sql.functions import mode
from . import models
from .database import engine, get_db
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
from random import randrange
from os.path import join, dirname
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
import psycopg2
import os


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
get_db()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

HOST = os.environ.get("host")
DATABASE = os.environ.get("database")
USER = os.environ.get("user")
PASSWORD = os.environ.get("password")


while True:
    try:
        conn = psycopg2.connect(host=HOST, database=DATABASE,
                                user=USER, password=PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('DB Conn was successfull!')
        break
    except Exception as error:
        print(f"Error: {error}")
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT into posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    post.dict()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}