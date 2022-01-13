from fastapi import FastAPI
from .routers import post, user, auth

app = FastAPI()


# Load routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# Default Root route
@app.get("/")
async def root():
    return {"message": "Hello World"}
