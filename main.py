from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite foods", "content": "I like Pizza", "id": 2}
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return post_dict


@app.get("/posts/{id}")
def get_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return post
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} not found")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            my_posts.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} not found")


@app.put("/posts/{id}")
def update_post(id: int, my_post: Post):
    post_dict = my_post.dict()
    post_dict['id'] = id
    print(post_dict)
    for index, post in enumerate(my_posts):
        print(id)
        if post['id'] == id:
            my_posts[index] = post_dict
            return {"data": post_dict}
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")
