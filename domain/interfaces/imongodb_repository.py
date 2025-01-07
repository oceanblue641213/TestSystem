from abc import ABC, abstractmethod
from typing import Any, List

class iMongoDBRepository(ABC):
    @abstractmethod
    def find_by_id(self, collection: str, id: str) -> Any:
        pass

    @abstractmethod
    def save(self, collection: str, entity: Any) -> Any:
        pass