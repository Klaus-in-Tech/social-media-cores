from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/posts")
def get_posts():
    return {"data": "This is your data"}

@app.post("/createpost")
def createpost(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}