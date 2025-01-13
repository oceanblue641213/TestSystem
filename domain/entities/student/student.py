import uuid
from django.db import models
from domain.entities.baseModel import BaseModel
from uuid import UUID, uuid4
from typing import Optional
from django.core.exceptions import ValidationError

class Student(BaseModel):
    #region ORM 欄位（Fields）
    _id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    _name = models.CharField(
        max_length=100,
        null=False,
        blank=False
        )
    _gender = models.CharField(
        max_length=1,
        choices=[
            ('M', 'Male'),
            ('F', 'Female')
        ],
        null=False,
        blank=False
    )
    _age = models.IntegerField(
        null=False,
        blank=False
        )
    _status = models.BooleanField(
        default=True
        )
    _avatarPath = models.CharField(
        max_length=255, blank=True
        )
    _documentPath = models.CharField(
        max_length=255, blank=True
        )
    
    #endregion
    
    def __init__(self, name: str, gender: str, age: int, id: Optional[UUID] = None):
        self.id = id or uuid4()
        self.name = name
        self.gender = gender
        self.age = age
        super().__init__()

    #region Domain Events
    def TriggerUpdateName(self, new_name: str, new_age: int) -> None:
        """更新名字的領域事件"""
        self.name = new_name
        self.age = new_age

    def TriggerCreate(self) -> None:
        """創建學生的領域事件"""
        pass
    
    #endregion
    
    #region 驗證事件
    def _validate_CREATE(self, *args, **kwargs) -> bool:
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
        app_label = 'application'  # 對應到你的 app name
        db_table = 'Student'
        managed = True
        ordering = ['-create_date']  # 預設排序

    #region Dunder Methods
    # 可選：自定義 __str__ 方法，用於在 admin 介面或印出物件時顯示
    def __str__(self):
        return f"{self.name} ({self.id})"
    #endregion

# 創建模型後
# python manage.py makemigrations
# python manage.py migrate
# 來創建數據庫表