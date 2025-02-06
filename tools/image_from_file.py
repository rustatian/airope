# Description: Read image from file
from abc import ABC

from autogen_core import CancellationToken
from autogen_core.tools import BaseTool

from shared.messages import ReadImageToolRequest, ReadImageToolReturn


class ImageReaderTool(BaseTool[ReadImageToolRequest, ReadImageToolRequest], ABC):
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
    ) -> bytes:
        with open(args.path, "rb") as f:
            return f.read()
