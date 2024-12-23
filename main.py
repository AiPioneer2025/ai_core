from typing import Union

from fastapi import FastAPI, APIRouter, Request, Response

# Import AI Module
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain.callbacks import AsyncIteratorCallbackHandler
from starlette.responses import StreamingResponse
from pydantic import BaseModel

import os
import asyncio

os.environ["ZHIPUAI_API_KEY"] = "34492d269e80b980eceaba735b5b0071.de7koKvFNhCkqpOc"

# Select Model
# 如果需要不停的交互，需要在Model里使用Callback
chat = ChatZhipuAI(
    model="glm-4",
    temperature=0.5,
)

from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

streaming_chat = ChatZhipuAI(
    model="glm-4",
    temperature=0.5,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

# 路由分组/ai_core/api
router = APIRouter()

userInput = (
    "你好，我今天梦见我在一个很高的钟楼上，下面全部都是要追杀我的人，请问这代表什么意思"
)


class RequestBody(BaseModel):
    userInput: str


@router.post("/query")
def query(request: RequestBody):
    messages = [
        AIMessage(content="您好，请描述您做的梦"),
        SystemMessage(content="你是一个周公解梦师。"),
        HumanMessage(content=request.userInput),
    ]
    response = chat.invoke(messages)
    return {"code": 200, "data": response.content, "msg": "success"}


@router.post("/query_stream")
async def query_stream(request: RequestBody):
    messages = [
        AIMessage(content="您好，请描述您做的梦"),
        SystemMessage(content="你是一个周公解梦师。"),
        HumanMessage(content=request.userInput),
    ]

    # 创建一个流式响应
    async def generate_stream():
        print(messages)
        try:
            async for chunk in chat.astream(messages):
                print(chunk.content, end="|", flush=True)
                yield chunk.content.encode("utf-8")
        except Exception as e:
            print(f"Error occurred during streaming: {e}")

    headers = {"Content-Type": "text/event-stream"}
    return StreamingResponse(generate_stream(), headers=headers)


app = FastAPI()
app.include_router(router, prefix="/ai_core/api")


@app.get("/")
def read_root():

    # 对userInput做调整

    # Prompt
    messages = [
        AIMessage(content="您好，请描述您做的梦"),
        SystemMessage(content="你是一个周公解梦师。"),
        HumanMessage(content=userInput),
    ]

    response = chat.invoke(messages)

    print(response)
    return {"modelResponse": response.content.replace("\n", "")}
