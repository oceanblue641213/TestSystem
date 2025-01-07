import uuid
from django.db import models
from django.utils import timezone
from domain.entities.baseModel import BaseModel
from django.core.exceptions import ValidationError
from dataclasses import dataclass, field

class EF(BaseModel):
    # 建構子（__init__ 方法）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    #region 私有欄位，但仍然可以映射到資料庫
    EFId = models.CharField(max_length=255, db_column='EFId', primary_key=True)  # 指定資料庫欄位名稱
    companyId: str = field(default='')
    name: str = field(default='')
    #endregion
    
    #region Django ORM 必須的欄位映射
    class Meta:
        db_table = 'EF'
        managed = True