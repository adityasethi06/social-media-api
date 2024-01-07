from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from pydantic import BaseModel
import psycopg2
from  psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    conn = psycopg2.connect(host="localhost",
                            database="socialmedia",
                            user="postgres",
                            password="root", 
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
except Exception as ex:
    raise RuntimeError(f"error connecting to DB: {ex}") 


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
                   (post.title, post.content, post.published))
    inserted_post = cursor.fetchone()
    conn.commit()
    return {"data": inserted_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response): # by adding type int, fastapi will take care of typcasting path param to int or throw error
    cursor.execute("SELECT * FROM posts WHERE id=%s", (str(id)))
    post = cursor.fetchone()
    if post:
        return {"data": post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No post found with id: {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"No post found with id: {id}"}
    
@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id)))
    deleted_psot = cursor.fetchone()
    if not deleted_psot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not there")
    conn.commit()
    return {"data": f"post with id: {id} deleted"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post, respone: Response):
    cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"posit with id: {id} not there")
    conn.commit()
    respone.status_code = status.HTTP_201_CREATED
    return {"data": updated_post}