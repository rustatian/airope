from autogen_core import RoutedAgent, message_handler, MessageContext

from shared.messages import TextMessage, ImageMessage


class RoutedBySenderAgent(RoutedAgent):
    @message_handler(match=lambda msg, ctx: msg.source.startswith("user1"))
    async def on_user1_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"hello from user1 handler, {message.source}, you said {message.content}")
        return None

    @message_handler(match=lambda msg, ctx: msg.source.startswith("user2"))
    async def on_user2_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"hello from user2 handler, {message.source}, you said {message.content}")
        return None

    @message_handler(match=lambda msg, ctx: msg.source.startswith("user2"))
    async def on_image_message(
        self, message: ImageMessage, ctx: MessageContext
    ) -> None:
        print(f"hello, {message.source}, you send me {message.url}")
        return None
