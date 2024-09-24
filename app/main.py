from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Annotated, Optional
from random import randrange
from app import database
from sqlalchemy.orm import Session
from app import database_models

app = FastAPI()

database

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},{"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/posts")

async def get_posts(db: Annotated[Session, Depends(database.get_db)]):
    my_posts = db.query(database_models.Posts).all()
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    post_dic = post.dict()
    post_dic['id'] = randrange(0,10000)
    my_posts.append(post_dic)
    return {"data": post_dic}

@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found.")
        
    return {"post details": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print(post)
    return {"data": post_dict}