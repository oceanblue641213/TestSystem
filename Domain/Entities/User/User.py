from django.db import models
from Domain.Entities.BaseModel import BaseModel
from django.core.exceptions import ValidationError

class User(BaseModel):
    #region 資料庫Schema
    class Meta:
        db_table = 'User'
        managed = True

    # 欄位（Fields）
    _Name = models.CharField(max_length=100)
    _Age = models.IntegerField()
    _Email = models.EmailField(unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    # 關係欄位
    # profile = models.OneToOneField(
    #     'Profile', 
    #     on_delete=models.CASCADE, 
    #     null=True, 
    #     related_name='user' # 使用related_name來方便反向查詢
    # )
    #endregion

    # 建構子（__init__ 方法）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # 可選：自定義 __str__ 方法，用於在 admin 介面或印出物件時顯示
    def __str__(self):
        return self.name
    
    