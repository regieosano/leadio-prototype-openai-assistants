from pydantic import BaseModel


class PostMessageRequest(BaseModel):
    chat: str


class PostMessageResponse(BaseModel):
    reply: str
