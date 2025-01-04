from django.apps import AppConfig
from .config import service_registry, app_config
from ..Infrastructure.persistence import MongoDBRepository

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Application'

    def ready(self):
        # 在 Django 應用啟動時初始化服務
        self.initialize_services()

    def initialize_services(self):
        # 獲取配置單例
        config = app_config.ServiceConfig.get_instance()
        # 初始化資料庫連接
        mongo_client = config.get_mongo_client()
        # mysql_client = config.get_mysql_client()
        # redis_client = config.get_redis_client()
        # 創建 repository 實例
        mongo = MongoDBRepository(mongo_client)
        # 註冊服務
        service_registry.ServiceRegistry.register("mongo", mongo)