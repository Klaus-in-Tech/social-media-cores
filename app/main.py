from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Annotated, Optional, List
from random import randrange
from app import database
from sqlalchemy.orm import Session
from app import database_models
from app import schemas

app = FastAPI()


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
@app.get("/posts",response_model=List[schemas.Post])
async def get_posts(db:Session= Depends(database.get_db)):
    my_posts = db.query(database_models.Posts).all()
    return my_posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createpost(post: schemas.CreatePost , db:Session= Depends(database.get_db)):
    # post_dic = post.dict()
    # post_dic['id'] = randrange(0,10000)
    # my_posts.append(post_dic)
    new_post = database_models.Posts(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(database.get_db)):
    # print(id)
    # post = find_post(id)
   
    post = db.query(database_models.Posts).filter(database_models.Posts.id == id).first()
    print(post)

    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found.")
    return {"post details": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(database.get_db)):
    # index = find_index_post(id)
    post = db.query(database_models.Posts).filter(database_models.Posts.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.CreatePost, db: Session=Depends(database.get_db)):
    # index = find_index_post(id)
    
    post_query = db.query(database_models.Posts).filter(database_models.Posts.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    # my_posts[index] = post_dict
    # print(post)
    return post_query.first()