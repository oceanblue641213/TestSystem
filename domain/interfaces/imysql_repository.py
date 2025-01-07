from abc import ABC, abstractmethod
from typing import List, Optional, Type
from django.db.models import Model

class iMySQLRepository(ABC):
    @abstractmethod
    def find_all(self, model: Type[Model]) -> List[Model]:
        pass

    @abstractmethod
    def find_by_id(self, model: Type[Model], id: str) -> Optional[Model]:
        pass

    @abstractmethod
    def find_by_filter(self, model: Type[Model], **kwargs) -> List[Model]:
        pass

    @abstractmethod
    def create(self, model: Type[Model], data: dict) -> Model:
        pass

    @abstractmethod
    def update(self, instance: Model, data: dict) -> Model:
        pass

    @abstractmethod
    def delete(self, instance: Model) -> bool:
        pass