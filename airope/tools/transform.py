from abc import ABC
import logging

from autogen_core import CancellationToken
from autogen_core.tools import BaseTool

from shared.messages import TransformRequest, TransformResponse


_log = logging.getLogger(__name__)


class TransformerTool(BaseTool[TransformRequest, TransformResponse], ABC):
    """Read image from file"""

    def __init__(self):
        super().__init__(
            args_type=TransformRequest,
            return_type=TransformResponse,
            name="read_image_from_file",
            description="User requests transformer",
        )

    async def run(
        self, args: TransformRequest, cancellation_token: CancellationToken
    ) -> TransformResponse:
        _log.debug("transform request %s", args.request)

        return TransformResponse(response="foo")
