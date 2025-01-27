from autogen_core import (
    MessageContext,
    RoutedAgent,
    message_handler,
)

from shared.messages import TextMessage, ImageMessage


class MegaAgent(RoutedAgent):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    @message_handler
    async def on_text_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"hello {message.source}, received message: {message.content}")
        return None

    @message_handler
    async def on_image_message(
        self, message: ImageMessage, ctx: MessageContext
    ) -> None:
        print(f"hello {message.source}, received image message: {message.url}")
        return None
