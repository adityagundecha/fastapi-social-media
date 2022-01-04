from datetime import datetime, timedelta
import os
from os.path import dirname, join
from jose import JWTError, jwt
from dotenv import load_dotenv

# SECRET_KEY
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
SECRET_KEY = os.environ.get("secret")

# Algorithm
ALGORITHM = "HS256"

# Expiration
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token
