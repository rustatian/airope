from pydantic import BaseModel


class TextMessage(BaseModel):
    content: str


class ImageMessage(BaseModel):
    url: str
    source: str


class ReadImageToolRequest(BaseModel):
    path: str

    def __repr__(self) -> str:
        return f"ReadImageToolRequest(path={self.path})"

    def __str__(self) -> str:
        return f"ReadImageToolRequest(path={self.path})"

    def __format__(self, format_spec: str) -> str:
        return f"ReadImageToolRequest(path={self.path})"


class ReadImageToolReturn(BaseModel):
    image: bytes
