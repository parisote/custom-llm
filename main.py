from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    model: str
    messages: list = []
    temperature: float


@app.get("/health")
def read_root():
    return {"Hello": "World Tom"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/v1/chat/completions")
def chat_openai(item: Item):
    print(item)
    return item