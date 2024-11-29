from abc import ABC, abstractmethod

class NetworkOperation(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Metodo base per tutte le strategie."""
        pass
