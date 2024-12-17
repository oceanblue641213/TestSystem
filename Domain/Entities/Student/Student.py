import uuid
from django.db import models
from django.utils import timezone
from Domain.Entities.BaseModel import BaseModel
from django.core.exceptions import ValidationError
from dataclasses import dataclass, field

class Student(BaseModel):
    # 建構子（__init__ 方法）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    #region 私有欄位，但仍然可以映射到資料庫
    _Id: uuid.UUID = field(default_factory=uuid.uuid4)
    _Name: str = field(default='')
    _Age: int = field(default=0)
    _Status: bool = field(default=True)
    _EmissionValue: float = field(default=0.0)
    _CreateDate: timezone.datetime = field(default_factory=timezone.now)
    _AvatarPath: str = field(default='')
    _DocumentPath: str = field(default='')
    #endregion
    
    #region Django ORM 必須的欄位映射
    class Meta:
        db_table = 'Student'
        managed = True

    # 欄位（Fields）
    Id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    CreateDate = models.DateTimeField(
        default=timezone.now
        )
    Status = models.BooleanField(
        default=True
        )
    EmissionValue = models.DecimalField(
        max_digits=12, 
        decimal_places=6
        )
    Name = models.CharField(
        max_length=100
        )
    Age = models.IntegerField(
        default=0
        )
    AvatarPath = models.CharField(
        max_length=255, blank=True
        )
    DocumentPath = models.CharField(
        max_length=255, blank=True
        )
    
    #endregion

    #region Dunder Methods
    # 可選：自定義 __str__ 方法，用於在 admin 介面或印出物件時顯示
    def __str__(self):
        return self._Name
    #endregion
    
    #region 對外事件
    def TriggerCreate(self, name: str, age: int):
        # 創建學生的主邏輯
        self._Name = name
        self._Age = age
        self.save()
    
    def TriggerUpdate(self, name: str = None, age: int = None, **kwargs):  # **kwargs 表示任意數量的關鍵字參數，建議將必填資料放在前面
        # 更新學生的主邏輯
        if name:
            self._Name = name
        if age is not None:
            self._Age = age
        
        # # 處理頭像上傳
        # if avatar_file:
        #     avatar_path = UserFileService.handle_user_avatar_upload(
        #         self, avatar_file
        #     )
        #     self._AvatarPath = avatar_path
    
        # # 處理文件上傳
        # if document_file:
        #     document_path = UserFileService.handle_user_document_upload(
        #         self, document_file
        #     )
        #     self._DocumentPath = document_path
            
        #     # 如果還有其他未處理的參數
        #     for key, value in kwargs.items():
        #         setattr(self, key, value)
        
        self.save()
    
    #endregion
    
    #region 驗證事件
    def _validate_create(self, name: str, age: int) -> bool:  # 驗證返回值建議都傳 bool
        # 創建學生的特定驗證邏輯
        if len(name) < 3:
            print("name too short")
            return False
        if not age:
            print("age is required")
            return False
        return True
    
    def _validate_update(self, **kwargs) -> bool:
        # 更新學生的特定驗證邏輯
        if 'name' in kwargs and len(kwargs['name']) < 3:
            print("name too short")
            return False
        return True
    #endregion
    

# 創建模型後
# python manage.py makemigrations
# python manage.py migrate
# 來創建數據庫表