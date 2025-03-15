# Description: Read image from file
import logging
from abc import ABC

from autogen_core import CancellationToken
from autogen_core.tools import BaseTool
from docling.document_converter import DocumentConverter

from airope.shared.messages import ReadImageToolRequest, ReadImageToolReturn

_log = logging.getLogger(__name__)


class ImageReaderTool(BaseTool[ReadImageToolRequest, ReadImageToolReturn], ABC):
    """Read image from file"""

    def __init__(self):
        super().__init__(
            args_type=ReadImageToolRequest,
            return_type=ReadImageToolReturn,
            name="read_image_from_file",
            description="Recognize content of the image/pdf by the provided path",
        )

    @classmethod
    async def foo(cls):
        pass

    async def run(
        self, args: ReadImageToolRequest, cancellation_token: CancellationToken
    ) -> ReadImageToolReturn:
        _log.debug("reading data from file %s", args.path)
        converter = DocumentConverter()
        result = converter.convert(args.path)
        data = result.document.export_to_text()
        return ReadImageToolReturn(text=data)
