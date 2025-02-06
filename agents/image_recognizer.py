import logging
from typing import Optional, List, Any, Callable, Awaitable

from autogen_agentchat.agents import AssistantAgent
from autogen_core import (
    RoutedAgent,
    MessageContext,
    message_handler,
    EVENT_LOGGER_NAME,
    AgentId,
)
from autogen_core.models import ModelFamily, LLMMessage, SystemMessage, UserMessage
from autogen_core.tool_agent import tool_agent_caller_loop
from autogen_core.tools import FunctionTool, BaseTool, ToolSchema
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import TRACE_LOGGER_NAME

from shared.messages import ImageMessage, TextMessage


class ImageRecognizerAgent(RoutedAgent):
    def __init__(
        self,
        name: str,
        model: str,
        api_key: str,
        base_url: str,
        family: ModelFamily,
        # tools: (
        #     List[
        #         BaseTool[Any, Any] | Callable[..., Any] | Callable[..., Awaitable[Any]]
        #     ]
        #     | None
        # ) = None,
        tools_schema: List[ToolSchema] | None = None,
    ):
        super().__init__("An image recognizer agent")
        model_client = OpenAIChatCompletionClient(
            model=model,
            api_key=api_key,
            base_url=base_url,
            model_info={
                "function_calling": True,
                "json_output": False,
                "vision": False,
                "family": family,
            },
        )

        self._tools_schema = tools_schema or []
        self._model_client = model_client
        self.logger = logging.getLogger(f"{EVENT_LOGGER_NAME}.image_recognizer")
        self._system_message: List[LLMMessage] = [
            SystemMessage(content="You're helpful AI assistant")
        ]
        self._tool_agent_id = AgentId(name, self.id.key)

    @message_handler
    async def handle_image(
        self, message: TextMessage, ctx: MessageContext
    ) -> TextMessage:
        logging.debug(f"Received image message: {message.content}")

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
        logging.debug(f"Received messages: {messages[-1].content}")

        return TextMessage(content=messages[-1].content)
