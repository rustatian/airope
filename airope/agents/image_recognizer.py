import logging

from autogen_agentchat.messages import TextMessage
from autogen_core import (
    EVENT_LOGGER_NAME,
    AgentId,
    MessageContext,
    RoutedAgent,
    message_handler,
)
from autogen_core.models import LLMMessage, ModelFamily, SystemMessage, UserMessage
from autogen_core.tool_agent import tool_agent_caller_loop
from autogen_core.tools import ToolSchema
from autogen_ext.models.ollama import OllamaChatCompletionClient

_log = logging.getLogger(__name__)


class ImageRecognizerAgent(RoutedAgent):
    """An agent that recognizes images."""

    def __init__(
        self,
        tool_agent_name: str,
        model: str,
        tools_schema: list[ToolSchema] | None = None,
    ):
        super().__init__("An image recognizer agent")
        model_client = OllamaChatCompletionClient(
            model=model,
            model_info={
                "function_calling": True,
                "json_output": False,
                "vision": False,
                "family": ModelFamily.UNKNOWN,
            },
        )

        self._tools_schema = tools_schema or []
        self._model_client = model_client
        self.logger = logging.getLogger(f"{EVENT_LOGGER_NAME}.image_recognizer")
        self._system_message: list[LLMMessage] = [
            SystemMessage(content="You're helpful AI assistant")
        ]
        self._tool_agent_id = AgentId(tool_agent_name, self.id.key)

    @message_handler
    async def handle_image(self, message: TextMessage, ctx: MessageContext) -> str:
        """Handle an image message."""

        _log.debug("Received image message: %s", {message.content})

        session = self._system_message + [
            UserMessage(content=message.content, source="user")
        ]

        messages = await tool_agent_caller_loop(
            self,
            tool_agent_id=self._tool_agent_id,
            model_client=self._model_client,
            tool_schema=self._tools_schema,
            cancellation_token=ctx.cancellation_token,
            input_messages=session,
        )

        _log.debug("received messages: %s", messages[-1].content)

        return str(messages[-1].content)
