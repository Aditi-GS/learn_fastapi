from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "I have no idea what to type :("}

@app.post("/posts")
def create_post(post: Post):
    return  {"data": post.model_dump()}