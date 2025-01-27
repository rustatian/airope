import asyncio
import logging
from dataclasses import dataclass

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
)
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.assistant import MyAssistant
from agents.broadcast_agent import BroadcastingAgent
from agents.direct_send import InnerAgent, OuterAgent
from agents.mega_agent import MegaAgent
from agents.routed_agent import RoutedBySenderAgent
from agents.subscribe_agent import ReceivingAgent
from shared.messages import TextMessage, ImageMessage


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
    """Mimic OpenAI"""
    return OpenAIChatCompletionClient(
        model="deepseek-r1:32b",
        api_key="ollama",
        base_url="http://0.0.0.0:11434/v1",
        model_capabilities={
            "json_output": False,
            "vision": False,
            "function_calling": True,
        },
    )


async def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(TRACE_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    logger.debug("Starting the runtime")

    ## different messages
    # runtime = SingleThreadedAgentRuntime()
    # await RoutedBySenderAgent.register(
    #     runtime, "my_agent", lambda: RoutedBySenderAgent("Routed")
    # )
    # runtime.start()
    #
    # agent_id = AgentId("my_agent", "default")
    #
    # await runtime.send_message(
    #     TextMessage(content="Hello, World!", source="user1-test"), agent_id
    # )
    # await runtime.send_message(
    #     TextMessage(content="Hello, World!", source="user2-test"), agent_id
    # )
    # await runtime.send_message(
    #     ImageMessage(url="https://example.com/image.jpg", source="user1-test"), agent_id
    # )
    # await runtime.send_message(
    #     ImageMessage(url="https://example.com/image.jpg", source="user2-test"), agent_id
    # )

    # runtime = SingleThreadedAgentRuntime()
    # await InnerAgent.register(runtime, "inner", lambda: InnerAgent("Inner"))
    # await OuterAgent.register(runtime, "outer", lambda: OuterAgent("Outer", "inner"))
    # runtime.start()
    # outer_agent_id = AgentId("outer", "default")
    # await runtime.send_message(
    #     TextMessage(content="Hello, World!", source="runtime"), outer_agent_id
    # )
    #
    # await runtime.stop_when_idle()

    ## Broadcast
    runtime = SingleThreadedAgentRuntime()

    # Option 1: with type_subscription decorator
    # The type_subscription class decorator automatically adds a TypeSubscription to
    # the runtime when the agent is registered.
    # await ReceivingAgent.register(
    #     runtime, "receiving_agent", lambda: ReceivingAgent("Receiving Agent")
    # )

    # Option 2: with TypeSubscription
    await BroadcastingAgent.register(
        runtime, "broadcasting_agent", lambda: BroadcastingAgent("Broadcasting Agent")
    )
    await runtime.add_subscription(
        TypeSubscription(topic_type="default", agent_type="broadcasting_agent")
    )

    # Start the runtime and publish a message.
    runtime.start()
    await runtime.publish_message(
        TextMessage(content="Hello, World! From the runtime!", source="runtime"),
        topic_id=TopicId(type="default", source="default"),
    )
    await runtime.stop_when_idle()

    # cathy = await Assistant.register(
    #     runtime,
    #     "cathy",
    #     lambda: Assistant(name="Cathy", model_client=get_model_client()),
    # )
    #
    # joe = await Assistant.register(
    #     runtime,
    #     "joe",
    #     lambda: Assistant(name="Joe", model_client=get_model_client()),
    # )

    # await MyAssistant.register(
    #     runtime,
    #     "assistant_1",
    #     lambda: MyAssistant(name="Assistant", model_name="deepseek-r1:32b"),
    # )
    #
    # await MegaAgent.register(
    #     runtime,
    #     "assistant_2",
    #     lambda: MegaAgent(name="Mega"),
    # )
    #
    # AgentType(type="assistant_1")

    # runtime.start()
    # await runtime.send_message(
    #     Message("Joe tell me a joke"),
    #     recipient=AgentId(joe, "default"),
    #     sender=AgentId(cathy, "default"),
    # )

    # agent_id = AgentId("assistant_2", "default")
    #
    # await runtime.send_message(
    #     TextMessage(
    #         content="What are you doing?",
    #         source="User",
    #     ),
    #     agent_id,
    # )
    #
    # await runtime.send_message(
    #     ImageMessage(url="https://example.com/image.jpg", source="User"), agent_id
    # )


if __name__ == "__main__":
    asyncio.run(main())
