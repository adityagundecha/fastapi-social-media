from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

HOST = os.environ.get("host")
DATABASE = os.environ.get("database")
USER = os.environ.get("user")
PASSWORD = os.environ.get("password")


SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
