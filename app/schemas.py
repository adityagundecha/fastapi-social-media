from pydantic import BaseModel

class Post(BaseModel):
    """A Class to define the shape of the requests coming into the API"""
    title: str
    content: str
    published: bool = True
