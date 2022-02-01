from datetime import datetime, timedelta
import os
from os.path import dirname, join
from jose import JWTError, jwt
from dotenv import load_dotenv
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
SECRET_KEY = os.environ.get("SECRET_KEY")

# Algorithm
ALGORITHM = "HS256"

# Expiration
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    print(f'token - {token}')
    return token


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})
    token = verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
