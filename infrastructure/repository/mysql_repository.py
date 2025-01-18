from typing import Type, TypeVar, Any
import asyncio
import logging
from typing import List, Optional, Type
from django.db import models
from domain.interfaces.imysql_repository import iMySQLRepository
from django.db.backends.mysql.base import DatabaseWrapper
from django.db import transaction
import domain.exceptions.exceptions as exceptions
from django.db import transaction
from asgiref.sync import sync_to_async
from django.utils import timezone
from uuid import UUID

T = TypeVar('T', bound=models.Model)

class MySQLRepository(iMySQLRepository):
    def __init__(self, mysql_client: DatabaseWrapper):
        self.client = mysql_client
        self.logger = logging.getLogger('infrastructure')

    async def find_by_id_async(self, model: Type[T], id: str) -> Optional[T]:
        try:
            # 將字符串 id 轉換為 UUID
            uuid_id = UUID(id)
            
            return await asyncio.to_thread(
                lambda: model.objects.using(self.client.alias).get(id=uuid_id)
            )
        except ValueError:
            # UUID 格式無效
            raise exceptions.RepositoryError(f"Invalid UUID format: {id}")
        except model.DoesNotExist:
            return None
        except Exception as e:
            self.logger.error(f"Error finding entity by id: {str(e)}")
            raise exceptions.RepositoryError(f"Failed to find entity: {str(e)}")

    async def save_async(self, entity: T) -> T:
        try:
            # 將整個事務操作包裝成同步函數
            @sync_to_async
            def save_with_transaction():
                with transaction.atomic():
                    # 檢查是否為新實體（改用 _state.adding）
                    is_new = entity._state.adding
                    
                    # 取得台北時區
                    current_time = timezone.now()
                    
                    if is_new:
                        entity.create_date = current_time
                        entity.updated_date = None
                    else:
                        entity.updated_date = current_time
                    entity.save()
                    
                    return entity
            
            # 執行事務
            saved_entity = await save_with_transaction()
            return saved_entity
            
        except Exception as e:
            self.logger.error(f"Error saving entity: {str(e)}")
            raise

    async def delete_async(self, entity: T) -> bool:
        try:
            result = await asyncio.to_thread(
                lambda: entity.delete(using=self.client.alias)
            )
            # Django 的 delete() 會返回一個元組 (刪除的物件數量, 詳細資訊字典)
            deleted_count, _ = result
            return deleted_count > 0
        except Exception as e:
            self.logger.error(f"Error deleting entity: {str(e)}")
            raise exceptions.RepositoryError(f"Failed to delete entity: {str(e)}")
    
    async def find_all_async(self, model: Type[T]) -> List[T]:
        return await asyncio.to_thread(
            lambda: list(model.objects.using(self.client.alias).all())
        )

    async def find_by_filter_async(self, model: Type[T], **kwargs) -> List[T]:
        return await asyncio.to_thread(
            lambda: list(model.objects.using(self.client.alias).filter(**kwargs))
        )