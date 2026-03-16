from random import randrange
from typing import Optional

from fastapi import FastAPI
from fastapi.param_functions import Body
from pydantic import BaseModel
from typing_extensions import Dict

app = FastAPI()


class Post(BaseModel):
    """This is class which defines the basemodel using pydantic to validate the input schema that the user should send"""

    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_val = [
    {"title1": "this is title 1", "content": "this is content 1", "id": 1},
    {"title2": "this is title 2", "content": "this is content 2", "id": 2},
]


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    return {"Data return": my_val}


@app.post("/createposts")
async def create_posts(payload: Dict = Body(...)):
    """payload is the variable of type dict, Body is a special function used to declare and validate request body parameters"""
    return {"payload": payload}


@app.post("/createpostsval")
async def create_posts_val(new_post: Post):
    """new_post is a variable, Post is from the class Post to validate the pydantic schema to check if the user is sending all the data in a type we expect"""
    print(new_post)
    new_post_dict = new_post.dict()
    return {"Valid": "Data upload is valid", "uploaded data is": new_post_dict}


@app.post("/posts")
async def create_post(post: Post):
    new_post_val = post.dict()
    new_post_val["id"] = randrange(0, 100000)
    my_val.append(new_post_val)
    return {"data upload successful": my_val}
