# Description: Read image from file
from abc import ABC
import logging

from autogen_core import CancellationToken
from autogen_core.tools import BaseTool

from shared.messages import ReadImageToolRequest, ReadImageToolReturn
from docling.document_converter import DocumentConverter


_log = logging.getLogger(__name__)


class ImageReaderTool(BaseTool[ReadImageToolRequest, ReadImageToolReturn], ABC):
    """Read image from file"""

    def __init__(self):
        super().__init__(
            args_type=ReadImageToolRequest,
            return_type=ReadImageToolReturn,
            name="read_image_from_file",
            description="Read image/doc/docs from the provided path",
        )

    async def run(
        self, args: ReadImageToolRequest, cancellation_token: CancellationToken
    ) -> ReadImageToolReturn:
        _log.debug("reading data from file %s", args.path)
        converter = DocumentConverter()
        result = converter.convert(args.path)
        data = result.document.export_to_text()
        _log.debug("data: %s", data)
        return ReadImageToolReturn(text=data)
