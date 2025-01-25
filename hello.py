import asyncio
from dataclasses import dataclass

from autogen_core import (
    AgentId,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    default_subscription,
    message_handler,
)
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    SystemMessage,
    UserMessage,
)
from autogen_ext.models.openai import OpenAIChatCompletionClient


@dataclass
class Message:
    content: str


@default_subscription
class Assistant(RoutedAgent):
    def __init__(self, name: str, model_client: ChatCompletionClient) -> None:
        super().__init__("An assistant agent")
        self._model_client = model_client
        self.name = name
        self.count = 0
        self._system_messages = [
            SystemMessage(content=f"You're helpful assistant, your name is {name}")
        ]
        self._model_context = BufferedChatCompletionContext(buffer_size=5)

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        self.count += 1
        await self._model_context.add_message(
            UserMessage(content=message.content, source="user")
        )

        result = await self._model_client.create(
            self._system_messages + await self._model_context.get_messages()
        )

        print(f"\n{self.name}: {message.content}")
        if "I need to go".lower() in message.content.lower() or self.count > 2:
            return

        await self._model_context.add_message(
            AssistantMessage(content=result.content, source="assistant")
        )
        await self.publish_message(Message(content=result.content), DefaultTopicId())


def get_model_client() -> OpenAIChatCompletionClient:
    "Mimic OpenAI"
    return OpenAIChatCompletionClient(
        model="deepseek-r1:70b",
        api_key="ollama",
        base_url="http://0.0.0.0:11434/v1",
        model_capabilities={
            "json_output": False,
            "vision": False,
            "function_calling": True,
        },
    )


async def main():
    runtime = SingleThreadedAgentRuntime()

    cathy = await Assistant.register(
        runtime,
        "cathy",
        lambda: Assistant(name="Cathy", model_client=get_model_client()),
    )

    joe = await Assistant.register(
        runtime,
        "joe",
        lambda: Assistant(name="Joe", model_client=get_model_client()),
    )
    runtime.start()
    try:
        await runtime.send_message(
            Message("Joe tell me a joke"),
            recipient=AgentId(joe, "default"),
            sender=AgentId(cathy, "default"),
        )
        await runtime.stop_when_idle()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
