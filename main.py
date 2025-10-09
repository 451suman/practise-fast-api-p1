from random import randrange
from typing import Optional
from fastapi import FastAPI, Header, Query, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel, Field

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: float = Field(..., ge=0, le=5)


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/")
def root():
    return {"message": "Heallo World!"}


@app.get("/items/")
def read_items(q: str = Query(None), x_token: str = Header(None)):
    breakpoint()
    return {"query": q, "X-Token": x_token}


# @app.post("/posts/{post_id}")
# def create_posts(post_id: int, post: Post):
#     if post.rating > 5:
#         return {"error": "rating must be less than 5"}
#     return {"post_id": post_id, "data": post}
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    post_dict["title"] = post.title + " " + str(post_dict["id"])
    my_posts.append(post_dict)
    return {"data": post_dict}


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # post = next(filter(lambda p: p["id"] == id, my_posts))
    post = find_post(id)
    if post == None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": "post not found"}
        # or you can do this
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post_id ": id, "data": post}


# @app.get("/posts/latest")
# this url match with above url so it will throw error
# it will match with id = "latest"
# @app.get("/posts/{id}")
# so to fix issue move "/posts/latest" to above above
# so it will match with post/latest berfore it match with post/{id}


from fastapi import Response, status


@app.delete("/posts/{id}")
def post_delete(id: int, response: Response):
    post = find_post(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    my_posts.remove(post)
    return {"message": "post deleted"}


@app.put("/posts/{id}")
def post_update(id: int, updated_post: Post):
    # Find the index of the post to update
    post_index = None
    for index, p in enumerate(my_posts):
        if p["id"] == id:

            post_index = index
            print("-------------------------------")
            print(p)
            print(post_index)
            print("-------------------------------")
            break

    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    # Convert updated_post to dict and keep the id unchanged
    post_dict = updated_post.dict()
    post_dict["id"] = id

    # Update the post at the found index
    my_posts[post_index] = post_dict

    return {"data": post_dict}
