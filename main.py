from ast import List
import asyncio
import logging
from fastapi import FastAPI

from autogen_core import (
    TRACE_LOGGER_NAME,
    AgentId,
    SingleThreadedAgentRuntime,
)
from autogen_core.tool_agent import ToolAgent
from openai.types.beta.thread_create_and_run_params import Tool

from agents.image_recognizer import ImageRecognizerAgent
from shared.messages import TextMessage
from tools.image_from_file import ImageReaderTool, read_image_tool


async def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(TRACE_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    logger.debug("Starting the runtime")
    runtime = SingleThreadedAgentRuntime()

    tools = [ImageReaderTool()]

    await ImageRecognizerAgent.register(
        runtime,
        "tool_use_agent",
        lambda: ImageRecognizerAgent(
            "tool_executor_agent",
            "llama3.3:70b",
            "placeholder",
            "http://127.0.0.1:11434/v1",
            [tool.schema for tool in tools],
        ),
    )

    await ToolAgent.register(
        runtime,
        "tool_executor_agent",
        lambda: ToolAgent("tool execute agent", tools=tools),  # type: ignore
    )

    runtime.start()

    await runtime.send_message(
        TextMessage(content="read image from file /Users/file.txt"),
        AgentId("tool_use_agent", "default"),
    )

    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
