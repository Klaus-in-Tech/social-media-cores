from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},{"title": "title of post 2", "content": "content of post 2", "id": 2}]

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/posts")
def get_posts():
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

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p