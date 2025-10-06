from typing import Optional
from fastapi import FastAPI, Header, Query
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/post")
def get_posts():
    return {"data": f"this is a post. "}


@app.get("/")
def root():
    return {"message": "Heallo World!"}


@app.get("/items/")
def read_items(q: str = Query(None), x_token: str = Header(None)):
    breakpoint()
    return {"query": q, "X-Token": x_token}


@app.post("/createposts/{post_id}")
def create_posts(post_id: int, post: Post):
    if post.rating > 5:
        return {"error": "rating must be less than 5"}
    # print(new_post)

    return {"post_id": post_id, "data": post}
