from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host="~~",
            database="~~",
            user="~~",
            password="~~",
            port="5433",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("DB connection successful!")
        break
    except psycopg2.Error as e:
        print("Database connection failed")
        print("Error:", e)
        time.sleep(2)

class Post(BaseModel):
    id: int = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

def find_post_by_id(id: int):
    query = """SELECT * FROM posts WHERE id=%s"""
    cursor.execute(query, vars=(id,))
    post = cursor.fetchone()
    return post 

@app.get("/")
def root():
    return {"message": "I have no idea what to type :("}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING
                   * """, (post.title, post.content, post.published, post.rating))
    new_post = cursor.fetchone()
    conn.commit()
    return  {"data": new_post}

@app.get("/posts")
def get_all_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/latest")
def get_latest_post():
    # query = """SELECT * FROM posts WHERE id = (SELECT MAX(id) FROM posts)"""
    # Below is Faster by ~ 15 ms
    query = """SELECT * FROM posts ORDER BY id DESC LIMIT 1"""
    cursor.execute(query)
    post = cursor.fetchone()
    return post

@app.get("/posts/{id}")
def get_post_by_id(id: int):
    post = find_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yo post {id} doesn't exist man !")
        # Response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Yo post {id} doesn't exist man !"}
    return post

# <-------------- ANOTHER WAY TO DELETE but 2 Queries -------------->
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post_by_id(id: int):
#     post = find_post_by_id(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Yo post {id} doesn't exist man !") 
#     query = """DELETE FROM posts WHERE id = %s"""
#     cursor.execute(query, vars=(id,))     
#     conn.commit()  
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int):
    query = """DELETE FROM posts WHERE id = %s RETURNING * """
    cursor.execute(query, vars=(id,)) 
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yo post {id} doesn't exist man !") 
    conn.commit()  
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post_by_id(id: int, post: Post):
    query = """UPDATE posts SET title=%s, content=%s, published=%s, rating=%s WHERE id = %s RETURNING * """
    values = (post.title, post.content, post.published, post.rating, id)
    cursor.execute(query, values)
    update_post = cursor.fetchone()
    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yo post {id} doesn't exist man !")  
      
    conn.commit()
    return update_post