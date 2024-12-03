from django.db import models
import Students.CommandEvents as Event

class Student(models.Model):
    #region 資料庫Schema
    class Meta:
        db_table = 'Student'
        managed = True

    # 欄位（Fields）
    Name = models.CharField(max_length=100)
    Age = models.IntegerField()
    Email = models.EmailField(unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    #endregion

    # 建構子（__init__ 方法）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def Trigger(self, e: Event.StudentCreate):
        self.name = e.name
        self.age = e.age
        self.email = e.email
        

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

    # 可選：自定義 __str__ 方法，用於在 admin 介面或印出物件時顯示
    def __str__(self):
        return self.name
    # endregion

    #region 屬性(Properties) Get/Set
    @property
    def name(self):
        return self.Name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) > 100:
            raise ValueError("Name is too long")
        self.Name = value  # 同步更新 Model 的 Name 欄位
    
    @property
    def age(self):
        return self.Age
    
    @age.setter
    def age(self, value):
        self.Age = value  # 同步更新 Model 的 Age 欄位

    @property
    def email(self):
        return self.Email
    
    @email.setter
    def email(self, value):
        self.Email = value  # 同步更新 Model 的 Email 欄位
    #endregion
    
# 創建模型後
# python manage.py makemigrations
# python manage.py migrate
# 來創建數據庫表