from typing import Union

from fastapi import FastAPI

# Import AI Module
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

import os

os.environ["ZHIPUAI_API_KEY"] = "34492d269e80b980eceaba735b5b0071.de7koKvFNhCkqpOc"

# Select Model
chat = ChatZhipuAI(
    model="glm-4",
    temperature=0.5,
)

# Prompt
messages = [
    AIMessage(content="您好，请描述您做的梦"),
    SystemMessage(content="你是一个周公解梦师。"),
    HumanMessage(content="我是一个男性，梦见自己生了一个男孩，请问一下这代表了什么？"),
]



app = FastAPI()


@app.get("/")
def read_root():
    response = chat.invoke(messages)
    print(response.content)  # Displays the AI-generated poem
    return response.content


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}