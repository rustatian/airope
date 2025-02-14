# Description: Read image from file
from abc import ABC

from autogen_core import CancellationToken
from autogen_core.tools import BaseTool
from autogen_core.tools import FunctionTool

from shared.messages import ReadImageToolRequest, ReadImageToolReturn

async def read_image(file: str) -> bytes:
    with open(file, "rb") as f:
        return f.read()


read_image_tool = FunctionTool(func=read_image, description="Read image from file")


class ImageReaderTool(BaseTool[ReadImageToolRequest, ReadImageToolReturn], ABC):
    """Read image from file"""

    def __init__(self):
        super().__init__(
            args_type=ReadImageToolRequest,
            return_type=ReadImageToolReturn,
            name="read_image_from_file",
            description="Read image from file",
        )

    async def run(
        self, args: ReadImageToolRequest, cancellation_token: CancellationToken
    ) -> ReadImageToolReturn:
        with open(args.path, "rb") as f:
            return ReadImageToolReturn(image=f.read())
