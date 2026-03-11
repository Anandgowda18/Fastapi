from fastapi import FastAPI
from fastapi.param_functions import Body
from typing_extensions import Dict

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    return {"information": "This is your post"}


@app.post("/createposts")
async def create_posts(payload: Dict = Body(...)):
    """payload is the variable of type dict, Body is a special function used to declare and validate request body parameters"""
    return {"payload": payload}
