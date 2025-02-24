from abc import ABC, abstractmethod

class ParserInterface(ABC):
    @abstractmethod
    def clean_and_join(self, buffer):
        """parser buffer."""
        pass
   
    
