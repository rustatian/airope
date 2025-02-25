from abc import ABC, abstractmethod


class ImageReader(ABC):
    def __init__(self, description: str):
        self._description = description

    @abstractmethod
    async def read_image(self):
        pass

    @abstractmethod
    async def get_description(self):
        pass
