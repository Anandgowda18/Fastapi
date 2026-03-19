from random import randrange
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
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


def my_val_return(id):
    for i in my_val:
        if i["id"] == id:
            return i


def my_val_index(id):
    for i, j in enumerate(my_val):
        if j["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/postsval")
async def get_posts():
    return {"Data return": my_val}


@app.post("/createposts")
async def create_posts(payload: Dict = Body(...)):
    """payload is the variable of type dict, Body is a special function used to declare and validate request body parameters"""
    return {"payload": payload}


@app.post("/createpostsval")
async def create_posts_val(new_post: Post):
    """new_post is a variable, Post is from the class Post to validate the pydantic schema to check if the user is sending all the data in a type we expect"""
    new_post_dict = new_post.dict()
    return {"Valid": "Data upload is valid", "uploaded data is": new_post_dict}


"""Below function will create a new post and assign an id to it.
adding/appending this post to my_val dictonary"""


@app.post("/posts")
async def create_post(post: Post):
    new_post_val = post.dict()
    new_post_val["id"] = randrange(0, 100000)
    my_val.append(new_post_val)
    return {"data upload successful": my_val}


"""Below function is to fetch the data using id in input(url)"""


@app.get("/posts/{id}")
async def get_value(id: int):
    if not my_val_return(id):
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"post with id {id} not found"}
        # you can replace the above code
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )
    return {"posts": my_val_return(id)}


"""Below function is to delete the data using id in input(url)"""


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_id(id: int):
    index = my_val_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    my_val.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = my_val_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_dict = post.dict()
    post_dict["id"] = id
    my_val[index] = post_dict
    return {"info": "Updated"}
