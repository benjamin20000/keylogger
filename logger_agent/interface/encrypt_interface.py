from abc import ABC, abstractmethod

class EncryptInteface(ABC):
    @abstractmethod
    def enc(self, messege):
        pass    