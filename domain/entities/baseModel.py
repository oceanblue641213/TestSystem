from django.db import models
from functools import wraps
from domain.enums.validationEventEnum import ValidationEvent
from django.utils import timezone

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
    class Meta:
        abstract = True  # 這是一個抽象基類，不會創建數據庫表
    
    """
    基礎模型，提供通用的欄位和方法
    """
    create_date = models.DateTimeField(
        default=timezone.now,  # 改用 timezone.now
        null=False,
        blank=False,
        editable=False
    )
    updated_date = models.DateTimeField(
        null=True,
        blank=True,
        editable=False
    )
    create_user_id = models.IntegerField(
        null=True,
        blank=True
    )
    is_deleted = models.BooleanField(
        default=False
    )

    def _get_event_type(self, method_name):
        # 根據方法名稱推斷事件類型
        if method_name.startswith('TriggerCreate'):
            return ValidationEvent.CREATE.value
        elif method_name.startswith('TriggerUpdate'):
            return ValidationEvent.UPDATE.value
        elif method_name.startswith('TriggerDelete'):
            return ValidationEvent.DELETE.value
        else:
            raise ValueError(f"未知 method type: {method_name}")

# 基礎驗證裝飾器
def validate_event(func):
    if isinstance(func, classmethod):
        orig_func = func.__get__(None, object).__func__
        
        @wraps(orig_func)
        def wrapper(cls, event, *args, **kwargs):
            # 獲取事件類型
            event_type = orig_func.__name__[7:].lower()
            
            # 獲取驗證方法
            validate_method = getattr(cls, f'_validate_{event_type}', None)
            if validate_method:
                event_dict = event.__dict__ if hasattr(event, '__dict__') else {}
                if not validate_method(**event_dict):
                    raise ValueError(f"Validation failed for {event_type}")
            
            return orig_func(cls, event, *args, **kwargs)
            
        return classmethod(wrapper)
    else:
        @wraps(func)
        def wrapper(self, event, *args, **kwargs):
            # 獲取事件類型
            event_type = func.__name__[7:].lower()
            
            # 獲取驗證方法
            validate_method = getattr(self.__class__, f'_validate_{event_type}', None)
            if validate_method:
                event_dict = event.__dict__ if hasattr(event, '__dict__') else {}
                if not validate_method(**event_dict):
                    raise ValueError(f"Validation failed for {event_type}")
            
            return func(self, event, *args, **kwargs)
        return wrapper

# field = models.FieldType(
#     null=False,          # 是否允許資料庫中的值為 NULL
#     blank=False,         # 是否允許表單驗證時為空值
#     default=None,        # 預設值
#     unique=False,        # 是否要求值唯一
#     db_index=False,      # 是否建立資料庫索引
#     help_text="說明文字", # 用於表單和文檔的說明文字
#     verbose_name="顯示名稱", # 在管理介面顯示的欄位名稱
#     primary_key=False,   # 是否為主鍵
#     editable=True,       # 是否可在管理介面編輯
#     choices=None,        # 選項列表，限制可選值
# )

# 字串欄位
# name = models.CharField(
#     max_length=100,      # 最大長度（必填）
#     min_length=None,     # 最小長度
#     db_collation=None,   # 資料庫排序規則
# )

# text = models.TextField(
#     max_length=None,     # 可選的最大長度限制
# )

# 數值欄位
# price = models.DecimalField(
#     max_digits=10,       # 最大位數（必填）
#     decimal_places=2,    # 小數位數（必填）
# )

# count = models.IntegerField(
#     validators=[],       # 自定義驗證器列表
# )

# 日期欄位
# create_date = models.DateTimeField(
#     auto_now_add=True,   # 創建時自動設置當前時間
#     auto_now=False,      # 每次儲存時更新時間
# )

# update_date = models.DateTimeField(
#     auto_now=True       # 每次更新時自動設置當前時間
# )

# 關聯欄位
# author = models.ForeignKey(
#     'Author',           # 關聯的模型
#     on_delete=models.CASCADE,  # 刪除時的行為
#     related_name='posts',      # 反向關聯名稱
#     related_query_name='post', # 反向查詢名稱
#     limit_choices_to={},       # 限制可選擇的關聯對象
# )

# tags = models.ManyToManyField(
#     'Tag',
#     through='PostTag',   # 中間表模型
#     symmetrical=False,   # 是否為對稱關係
# )

# 檔案欄位
# image = models.ImageField(
#     upload_to='images/', # 上傳路徑
#     height_field=None,   # 高度欄位名稱
#     width_field=None,    # 寬度欄位名稱
# )

# file = models.FileField(
#     upload_to='files/',  # 上傳路徑
#     storage=None,        # 自定義存儲後端
# )

# 布林欄位
# is_active = models.BooleanField(
#     default=True,        # 預設值
#     db_index=True,       # 建立索引以加速查詢
# )

# on_delete 選項
# models.CASCADE           # 刪除關聯對象時一併刪除
# models.PROTECT          # 阻止刪除有關聯的對象
# models.SET_NULL         # 設置為 NULL（需要 null=True）
# models.SET_DEFAULT      # 設置為預設值
# models.DO_NOTHING       # 不做任何處理