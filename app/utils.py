from os.path import dirname, join
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SQLALCHEMY_DATABASE_URL = ''


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_db_url():
    dotenv_path = join(dirname(__file__), '../.env')
    load_dotenv(dotenv_path)

    HOST = os.environ.get("DATABASE_HOSTNAME")
    DATABASE = os.environ.get("DATABASE_NAME")
    USER = os.environ.get("DATABASE_USERNAME")
    PASSWORD = os.environ.get("DATABASE_PASSWORD")
    SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
    return SQLALCHEMY_DATABASE_URL
