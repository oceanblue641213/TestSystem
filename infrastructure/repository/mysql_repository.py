from typing import Type, TypeVar, Any
import asyncio
import logging
from typing import List, Optional, Type
from django.db import models
from domain.interfaces.imysql_repository import iMySQLRepository
from django.db.backends.mysql.base import DatabaseWrapper

T = TypeVar('T', bound=models.Model)

class MySQLRepository(iMySQLRepository):
    def __init__(self, mysql_client: DatabaseWrapper):
        self.client = mysql_client
        self.logger = logging.getLogger('infrastructure')

    async def find_by_id_async(self, model: Type[T], id: str) -> Optional[T]:
        try:
            # 使用 asyncio.to_thread 將同步操作轉換為非同步
            return await asyncio.to_thread(
                lambda: model.objects.using(self.client.alias).get(id=id)
            )
        except model.DoesNotExist:
            return None

    async def save_async(self, entity: T) -> T:
        return await asyncio.to_thread(
            lambda: entity.save(using=self.client.alias)
        )

    async def delete_async(self, entity: T) -> bool:
        await asyncio.to_thread(
            lambda: entity.delete(using=self.client.alias)
        )
        return True
    
    async def find_all_async(self, model: Type[T]) -> List[T]:
        return await asyncio.to_thread(
            lambda: list(model.objects.using(self.client.alias).all())
        )

    async def find_by_filter_async(self, model: Type[T], **kwargs) -> List[T]:
        return await asyncio.to_thread(
            lambda: list(model.objects.using(self.client.alias).filter(**kwargs))
        )