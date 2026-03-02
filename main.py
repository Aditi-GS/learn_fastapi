from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return {"message": "I have no idea what to type :("}

@app.post("/posts")
def create_post(payload: dict = Body(...)):
    return {"new_post": f"Title: {payload['title']} AND Content: {payload['content']}"}