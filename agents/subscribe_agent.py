from autogen_core import RoutedAgent, message_handler, MessageContext, type_subscription

from shared.messages import TextMessage


@type_subscription(topic_type="default")
class ReceivingAgent(RoutedAgent):
    @message_handler
    async def on_my_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"received message: {message.content}, from {message.source}")
        return None
