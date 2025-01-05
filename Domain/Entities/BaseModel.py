from django.db import models
from typing import Callable, Any
from functools import wraps
from Domain.enums.validationEventEnum import ValidationEvent

# 通用模型基類的元類
class ValidationModelMeta(type(models.Model)):
    def __new__(mcs, name, bases, attrs):
        # 找出所有以 Trigger 開頭的方法
        trigger_methods = [
            method_name for method_name in attrs.keys() 
            if method_name.startswith('Trigger')
        ]
        
        # 為這些方法添加驗證裝飾器
        for method_name in trigger_methods:
            if method_name in attrs:
                attrs[method_name] = validate_event(attrs[method_name])
        
        return super().__new__(mcs, name, bases, attrs)

class BaseModel(models.Model, metaclass=ValidationModelMeta):
    """
    基礎模型，提供通用的欄位和方法
    """
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    create_user_id = models.IntegerField()

    class Meta:
        abstract = True  # 這是一個抽象基類，不會創建數據庫表
    
    def _get_event_type(self, method_name):
        # 根據方法名稱推斷事件類型
        if method_name.startswith('TriggerCreate'):
            return ValidationEvent.CREATE
        elif method_name.startswith('TriggerUpdate'):
            return ValidationEvent.UPDATE
        elif method_name.startswith('TriggerDelete'):
            return ValidationEvent.DELETE
        else:
            raise ValueError(f"未知 method type: {method_name}")

# 基礎驗證裝飾器
def validate_event(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # 確定當前觸發的事件類型
        event_type = self._get_event_type(func.__name__)
        
        # 執行驗證
        validation_method = getattr(self, f'_validate_{event_type}', None)
        if validation_method:
            validation_result = validation_method(*args, **kwargs)
            if validation_result is False:
                raise ValueError(f"Validation failed for event: {event_type}")
        
        # 執行原始方法
        return func(self, *args, **kwargs)
    return wrapper