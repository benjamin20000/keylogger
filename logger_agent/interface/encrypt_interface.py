from abc import ABC, abstractmethod

class EncryptInteface(ABC):
    @abstractmethod
    def encrypt(self, data):
        pass    


