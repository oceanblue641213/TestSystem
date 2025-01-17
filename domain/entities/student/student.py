import uuid
from django.db import models
from domain.entities.baseModel import BaseModel
from uuid import UUID, uuid4
from typing import Optional
from django.core.exceptions import ValidationError
import domain.events.student.commandEvents as commandEvents

class Student(BaseModel):
    #region ORM 欄位（Fields）
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False
        )
    gender = models.CharField(
        max_length=1,
        choices=[
            ('M', 'Male'),
            ('F', 'Female')
        ],
        null=False,
        blank=False
    )
    age = models.IntegerField(
        null=False,
        blank=False
        )
    
    #endregion
    
    def __init__(self, name: str, gender: str, age: int, id: Optional[UUID] = None):
        """新增的領域事件"""
        self.id = id or uuid4()
        self.name = name
        self.gender = gender
        self.age = age
        super().__init__()
    #region Domain Events
    def TriggerUpdated(self, event: commandEvents.StudentUpdated) -> None:
        """更新的領域事件"""
        self.name = event.name
        self.age = event.age
        self.gender = event.gender
    
    def TriggerDeleted(self, event: commandEvents.StudentDeleted) -> None:
        """刪除的領域事件"""
        self.is_deleted = True
    
    #endregion
    
    #region 驗證事件
    def _validate_create(self, *args, **kwargs) -> bool:
        """創建時的驗證"""
        if not self.gender in ['M', 'F']:
            raise ValidationError("性別必須是 M 或 F")
        if self.age < 0 or self.age > 150:
            raise ValidationError("年齡必須在 0-150 之間")
        if not self.name or len(self.name.strip()) == 0:
            raise ValidationError("名字不能為空")
        return True
    
    def _validate_update(self, **kwargs) -> bool:
        # 更新學生的特定驗證邏輯
        if 'name' in kwargs and len(kwargs['name']) < 3:
            print("name too short")
            return False
        return True

    #endregion
    
    class Meta:
        app_label = 'domain'  # 對應到你的 app name
        db_table = 'Student'
        managed = True
        ordering = ['-create_date']  # 預設排序

    #region Dunder Methods
    # 可選：自定義 __str__ 方法，用於在 admin 介面或印出物件時顯示
    def __str__(self):
        return f"{self.name} ({self.id})"
    #endregion

# 創建模型後
# python manage.py makemigrations domain
# python manage.py migrate domain
# 來創建數據庫表