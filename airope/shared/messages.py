from pydantic import BaseModel


class ReadImageToolRequest(BaseModel):
    path: str

    def __repr__(self) -> str:
        return f"ReadImageToolRequest(path={self.path})"

    __str__ = __repr__


class ReadImageToolReturn(BaseModel):
    text: str


class TransformRequest(BaseModel):
    request: str


class TransformResponse(BaseModel):
    response: str


class ZipRequest(BaseModel):
    path: str


class ZipResponse(BaseModel):
    path: str
