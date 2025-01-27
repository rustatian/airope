from pydantic import BaseModel


class TextMessage(BaseModel):
    content: str
    source: str


class ImageMessage(BaseModel):
    url: str
    source: str
