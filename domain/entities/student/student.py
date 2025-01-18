import uuid
from django.db import models
from domain.entities.baseModel import BaseModel, validate_event
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    @validate_event
    def TriggerCreated(cls, event: commandEvents.StudentCreated) -> 'Student':
        """創建新的 Student 實體"""
        instance = cls()
        instance.name = event.name
        instance.gender = event.gender
        instance.age = event.age
            
        return instance
    
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
    @staticmethod
    def _validate_created(name: str, gender: str, age: int, **kwargs) -> bool:
        """創建時的驗證"""
        if not gender in ['M', 'F']:
            raise ValidationError("性別必須是 M 或 F")
        if age < 0 or age > 150:
            raise ValidationError("年齡必須在 0-150 之間")
        if not name or len(name.strip()) == 0:
            raise ValidationError("名字不能為空")
        return True

    @staticmethod
    def _validate_updated(name: str, gender: str, age: int, **kwargs) -> bool:
        """更新時的驗證"""
        if not gender in ['M', 'F']:
            raise ValidationError("性別必須是 M 或 F")
        if age < 0 or age > 150:
            raise ValidationError("年齡必須在 0-150 之間")
        if not name or len(name.strip()) == 0:
            raise ValidationError("名字不能為空")
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