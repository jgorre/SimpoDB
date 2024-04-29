from abc import ABC, abstractmethod

class SqlCommand(ABC):
    @abstractmethod
    def execute(self):
        pass