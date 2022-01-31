from fastapi import FastAPI
from .database import engine
from .routers import auth, post, user, vote

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)


# Load routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Default Root route
@app.get("/")
async def root():
    return {"message": "Hello World"}
