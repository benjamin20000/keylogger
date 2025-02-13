from abc import ABC, abstractmethod

class WriterInterface(ABC):
    @abstractmethod
    def write(message: str) -> None:
        pass
