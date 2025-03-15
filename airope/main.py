import argparse
import asyncio
import logging

from autogen_agentchat.messages import TextMessage
from autogen_core import (
    AgentId,
    SingleThreadedAgentRuntime,
)
from autogen_core.tool_agent import ToolAgent

from agents.image_recognizer import ImageRecognizerAgent
from tools.recognize_from_file import ImageReaderTool

parser = argparse.ArgumentParser(description="AIRope CLI")
parser.add_argument("--log", type=str, default="DEBUG", help="Log level")

_log = logging.getLogger(__name__)
runtime = SingleThreadedAgentRuntime()


async def main():
    args = parser.parse_args()
    if args.log is not None:
        logging.basicConfig(level=args.log)
    else:
        logging.basicConfig(level=logging.DEBUG)

    tools = [ImageReaderTool()]

    _log.info("registering agents")
    await ImageRecognizerAgent.register(
        runtime,
        "tool_use_agent",
        lambda: ImageRecognizerAgent(
            "tool_executor_agent",
            "llama3.3:70b",
            [tool.schema for tool in tools],
        ),
    )

    _log.info("registering tool agent")
    await ToolAgent.register(
        runtime,
        "tool_executor_agent",
        lambda: ToolAgent("tool execute agent", tools=tools),  # type: ignore
    )

    _log.info("starting runtime")
    runtime.start()

    res = await runtime.send_message(
        TextMessage(
            content="read doc from file /Users/valery/Downloads/main_notes.pdf and tell what is about in no more than 10 words",
            source="user",
        ),
        AgentId("tool_use_agent", "default"),
    )

    _log.debug(f"result={res}")

    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
