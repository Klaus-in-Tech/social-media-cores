from fastapi import FastAPI
from .routers import user, post, auth
import uvicorn

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)