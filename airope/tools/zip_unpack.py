from abc import ABC
import logging

from autogen_core import CancellationToken
from autogen_core.tools import BaseTool

from shared.messages import ZipRequest, ZipResponse


_log = logging.getLogger(__name__)


class ZipUnpackTool(BaseTool[ZipRequest, ZipResponse], ABC):
    """Read image from file"""

    def __init__(self):
        super().__init__(
            args_type=ZipRequest,
            return_type=ZipResponse,
            name="unpack_zip",
            description="Unpacks a zip file",
        )

    async def run(
        self, args: ZipRequest, cancellation_token: CancellationToken
    ) -> ZipResponse:
        _log.debug("unpacking zip %s", args.path)
        # unpacking zip

        return ZipResponse(path="foo")
