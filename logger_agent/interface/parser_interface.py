from abc import ABC, abstractmethod

class ParserInterface(ABC):
    @abstractmethod
    def parse_data(self, buffer):
        """parser buffer."""
        pass
   
    
