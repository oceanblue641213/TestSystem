import pytz
import asyncio
import logging
from uuid import UUID
from ninja import Schema
from django.db import models
from django.utils import timezone
from django.db import transaction
from django.db import transaction
from asgiref.sync import sync_to_async
from typing import List, Optional, Type
from domain.dtos.sortDto import SortDto
from datetime import time, date, datetime
from django.core.paginator import Paginator
import domain.exceptions.exceptions as exceptions
from typing import Type, TypeVar, Any, List, Optional
from django.db.backends.mysql.base import DatabaseWrapper
from domain.interfaces.imysql_repository import iMySQLRepository

T = TypeVar('T', bound=models.Model)

class MySQLRepository(iMySQLRepository):
    def __init__(self, mysql_client: DatabaseWrapper):
        self.client = mysql_client
        self.logger = logging.getLogger('infrastructure')
    
    @staticmethod 
    def convert_value(value: Any) -> Any:
        """根據不同型別進行轉換"""
        if isinstance(value, UUID):
            return str(value)
        elif isinstance(value, datetime):
            # 如果是 UTC 時間，先轉換到本地時間
            if value.tzinfo is not None:
                local_dt = value.astimezone(pytz.timezone('Asia/Taipei'))
            else:
                local_dt = value
            # 轉換成指定格式
            return local_dt.strftime("%Y%m%d%H%M%S")
        elif isinstance(value, (date, time)):
            return str(value)
        # 可以添加其他型別的轉換邏輯
        return value
    
    async def find_by_params_async(
        self,
        model: Type[T],
        sort: SortDto,
        dto_class: Type[Schema],
    ) -> List[Schema]:
        """
        整合查詢功能的非同步函數
        
        Args:
        model: Django Model 類別
        sort: 查詢參數
        select_fields: 要選擇的特定欄位列表 (默認為None，表示選擇所有欄位)
        
        Sample:
        select_fields=['id', 'name', 'status']  # 只查詢特定欄位
        
        Returns:
            Dict 包含:
                - items: 查詢結果列表
                - total: 總筆數
                - total_pages: 總頁數
                - current_page: 當前頁碼
        """
        
        def execute_query():  # 移除 async
            # 建立基礎查詢
            query = model.objects.using(self.client.alias)
            
            # 加入篩選條件
            if sort.filters:
                query = query.filter(**sort.filters)
            
            # 從 DTO 類別獲取欄位名稱
            dto_fields = dto_class.model_fields.keys()
            
            # 處理排序
            if sort.order_by:
                if isinstance(sort.order_by, str):
                    order_by_fields = [sort.order_by]
                else:
                    order_by_fields = sort.order_by
                
                query = query.order_by(*order_by_fields)
            
            # 建立分頁器
            paginator = Paginator(query, sort.page_size)
            current_page = min(max(1, sort.page), paginator.num_pages)
            
            # 取得當前頁的資料
            page_obj = paginator.page(current_page)
            
            return [
                dto_class(**{
                    field: self.convert_value(getattr(item, field))
                    for field in dto_fields
                    if hasattr(item, field)
                })
                for item in page_obj.object_list
            ]
        
        try:
            # 直接等待 to_thread 的結果
            return await asyncio.to_thread(execute_query)
        except Exception as e:
            self.logger.error(f"查詢失敗: {str(e)}")
            raise

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
    