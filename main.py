import os

from groq import Groq
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

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="mixtral-8x7b-32768",
)

@app.get("/health")
def read_root():
    return {"Hello": "World Tom"}

@app.post("/v1/chat/completions", response_model=ChatCompletion)
def chat_openai(item: Item):
    print(item)
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
        ],
        model="mixtral-8x7b-32768",
    )
    print("RESPONSE")
    print(chat_completion)
    return chat_completion