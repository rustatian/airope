from autogen_core import RoutedAgent, message_handler, MessageContext, TopicId

from shared.messages import TextMessage


class BroadcastingAgent(RoutedAgent):
    @message_handler
    async def on_my_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"received message: {message.content}, from {message.source}")
        await self.publish_message(
            TextMessage(
                content=f"hello from broadcast, {message.content}", source="broadcast"
            ),
            topic_id=TopicId(type="default", source=self.id.key),
        )

        return None
