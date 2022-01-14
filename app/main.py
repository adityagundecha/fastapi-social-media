from fastapi import FastAPI
from .routers import post, user, auth
from .database import engine
from . import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Load routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# Default Root route
@app.get("/")
async def root():
    return {"message": "Hello World"}
