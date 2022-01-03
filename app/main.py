import os
import time
from os.path import dirname, join
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from .routers import post, user

app = FastAPI()


models.Base.metadata.create_all(bind=engine)
get_db()


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


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
