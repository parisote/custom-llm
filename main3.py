from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    model: str
    messages: list = []
    temperature: float

class Message(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    message: Message
    logprobs: Optional[None]
    finish_reason: str
    index: int

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletion(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: List[Choice]


@app.get("/health")
def read_root():
    return {"Hello": "World Tom"}

@app.post("/v1/chat/completions", response_model=ChatCompletion)
def chat_openai(item: Item):
    print(item)
    return {
    "id": "chatcmpl-abc123",
    "object": "chat.completion",
    "created": 1677858242,
    "model": "gpt-3.5-turbo-0613",
    "usage": {
        "prompt_tokens": 13,
        "completion_tokens": 7,
        "total_tokens": 20
    },
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "\n\nThis is a test!"
            },
            "logprobs": None,
            "finish_reason": "stop",
            "index": 0
        }
    ]
}