from autogen_core import RoutedAgent, message_handler, MessageContext, AgentId

from shared.messages import TextMessage


class InnerAgent(RoutedAgent):
    @message_handler
    async def on_my_message(
        self, message: TextMessage, ctx: MessageContext
    ) -> TextMessage:
        return TextMessage(
            content=f"hello from inner, message: {message.content}", source="inner"
        )


class OuterAgent(RoutedAgent):
    def __init__(self, description: str, inner_agent_type: str):
        super().__init__(description)
        self.inner_agent_id = AgentId(inner_agent_type, self.id.key)

    @message_handler
    async def on_my_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"received message: {message.content}, from {message.source}")
        # send a direct message to the inner agent
        response = await self.send_message(
            TextMessage(
                content=f"hello from outer, {message.content}",
                source=f"source: {message.source}",
            ),
            self.inner_agent_id,
        )
        print(f"received response: {response.content}")
