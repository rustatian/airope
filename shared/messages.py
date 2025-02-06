from pydantic import BaseModel


class TextMessage(BaseModel):
    content: str


class ImageMessage(BaseModel):
    url: str
    source: str


class ReadImageToolRequest(BaseModel):
    path: str


class ReadImageToolReturn(BaseModel):
    image: bytes
