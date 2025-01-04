from abc import ABC, abstractmethod
from typing import Any, List

class iMongoDB(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Any:
        pass

    @abstractmethod
    def save(self, entity: Any) -> Any:
        pass