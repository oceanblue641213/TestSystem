from django.db import models

class BaseModel(models.Model):
    """
    基礎模型，提供通用的欄位和方法
    """
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    create_user_id = models.IntegerField()

    class Meta:
        abstract = True  # 這是一個抽象基類，不會創建數據庫表