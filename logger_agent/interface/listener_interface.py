from abc import ABC, abstractmethod

class ListenerInterface(ABC):
    
    @abstractmethod
    def start(self, key_handler):
        """Keylogger starting."""
        pass
    @abstractmethod
    def stop(self):
        """Keylogger stopping."""
        pass
    
