from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreated(PostBase):
    """A Class to define the shape of the requests coming into the API"""
    pass


class PostResponse(PostBase):
    """A Class to define the shape of the response coming from the API"""
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """A Class to create a User"""
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    podt_id: int
    dir: conint(le=1)