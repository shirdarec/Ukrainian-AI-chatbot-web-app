# Import required modules
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from dotenv import load_dotenv, find_dotenv
from bot.essential_chain import initialize_chain

app = FastAPI()

qa = initialize_chain()


@app.get("/")
def read_root():
    return {"Detail": "Api for the Ukrainian bot"}


@app.get("/getresponse")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}