from fastapi import FastAPI
from server.routes.posts import router as PostRouter

app = FastAPI()

app.include_router(PostRouter, tags=["Post"], prefix="/post")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this dope app!"}