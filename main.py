import asyncio
import logging
from dataclasses import dataclass

from autogen_agentchat.agents import AssistantAgent
from autogen_core import (
    AgentId,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    default_subscription,
    message_handler,
    AgentType,
    TRACE_LOGGER_NAME,
    TypeSubscription,
    TopicId,
)
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    SystemMessage,
    UserMessage,
    ModelFamily,
)
from autogen_core.tool_agent import ToolAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.code_execution import PythonCodeExecutionTool

from agents.image_recognizer import ImageRecognizerAgent
from shared.messages import TextMessage, ImageMessage
from tools.image_from_file import ImageReaderTool


async def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(TRACE_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    logger.debug("Starting the runtime")
    runtime = SingleThreadedAgentRuntime()

    tools = [ImageReaderTool()]

    AssistantAgent

    await ImageRecognizerAgent.register(
        runtime,
        "tool_use_agent",
        lambda: ImageRecognizerAgent(
            "tool_use_agent",
            "llama3.3:70b",
            "placeholder",
            "http://127.0.0.1:11434/v1",
            ModelFamily.ANY,
            [tool.schema for tool in tools],
        ),
    )

    await ToolAgent.register(
        runtime,
        "tool_executor_agent",
        lambda: ToolAgent("tool execute agent", tools=tools),
    )

    runtime.start()

    await runtime.send_message(
        TextMessage(content="read image from file /Users/file.txt"),
        AgentId("tool_use_agent", "default"),
    )

    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
