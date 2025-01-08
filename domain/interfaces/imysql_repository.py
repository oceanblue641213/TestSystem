from typing import Type, TypeVar, Any
from abc import ABC, abstractmethod
from typing import List, Optional, Type
from django.db import models

T = TypeVar('T', bound=models.Model)

class iMySQLRepository(ABC):
    @abstractmethod
    async def find_by_id_async(self, model: Type[T], id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def save_async(self, entity: T) -> T:
        pass

    @abstractmethod
    async def delete_async(self, entity: T) -> bool:
        pass