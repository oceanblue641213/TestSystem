from django.db import models
from Domain.Entities.BaseModel import BaseModel
from django.core.exceptions import ValidationError
import Domain.Dtos.StudentDto as dto

class Student(BaseModel):
    #region 資料庫Schema
    class Meta:
        db_table = 'Student'
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
    #     related_name='User' # 使用related_name來方便反向查詢
    # )
    #endregion

    #建構子（__init__ 方法）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    #region 對外事件
    def create_student(self, e:dto.StudentDto):
        print("orm建立資料庫連線")
        
    def update_student(self, e:dto.StudentDto):
        print("orm建立資料庫連線")
    #endregion
    
    #region 資料驗證邏輯
    @staticmethod
    def validate_data(data):
        # 實作驗證邏輯
        if not data.get('name') or not data.get('age'):
            raise ValidationError("name and age are required")
        if '@' not in data.get('email', ''):
            raise ValidationError("Invalid email format")
        return True
    # endregion

    #region Dunder Methods
    # 可選：自定義 __str__ 方法，用於在 admin 介面或印出物件時顯示
    def __str__(self):
        return self.name
    #endregion

    #region 自定義方法（Function）
    def get_full_info(self):
        """
        返回學生的完整資訊
        """
        return f"Name: {self.name}, Age: {self.age}, Email: {self.email}"

    def is_adult(self):
        """
        檢查學生是否成年
        """
        return self.age >= 18
    # endregion

    #region 屬性(Properties) Get/Set
    @property
    def name(self):
        return self._Name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) > 100:
            raise ValueError("Name is too long")
        self._Name = value  # 同步更新 Model 的 Name 欄位
    
    @property
    def age(self):
        return self._Age
    
    @age.setter
    def age(self, value):
        self._Age = value  # 同步更新 Model 的 Age 欄位

    @property
    def email(self):
        return self._Email
    
    @email.setter
    def email(self, value):
        self._Email = value  # 同步更新 Model 的 Email 欄位
    #endregion
    

# 創建模型後
# python manage.py makemigrations
# python manage.py migrate
# 來創建數據庫表