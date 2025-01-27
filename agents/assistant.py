from autogen_agentchat.agents import AssistantAgent
from autogen_core import RoutedAgent, message_handler, MessageContext
from autogen_ext.models.openai import OpenAIChatCompletionClient

from shared.messages import TextMessage


class MyAssistant(RoutedAgent):
    """
    This is the agent that will be used to interact with the assistant agent.
    Args:
        name (str): The name of the agent.
        model_name (str): The name of the model to use
    """

    def __init__(self, name: str, model_name: str):
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(
            model="deepseek-r1:70b",
            api_key="ollama",
            base_url="http://0.0.0.0:11434/v1",
            model_capabilities={
                "json_output": False,
                "vision": False,
                "function_calling": True,
            },
        )

        self._delegate = AssistantAgent(name=name, model_client=model_client)

    @message_handler
    async def handle_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"{self.id.type}, received message: {message.content}")
        response = await self._delegate.on_messages(
            [TextMessage(content=message.content, source="user")],
            ctx.cancellation_token,
        )
        print(f"{self.id.type} responded: {response.chat_message.content}")
