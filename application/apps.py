from django.apps import AppConfig
from .config import service_registry, app_config
from infrastructure.repository.mongodb_repository import MongoDBRepository
from infrastructure.repository.redis_repository import RedisRepository
from infrastructure.repository.mysql_repository import MySQLRepository

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'

    def ready(self):
        import application.signals
        # 在 Django 應用啟動時初始化服務
        self.initialize_services()

    def initialize_services(self):
        # 獲取配置單例
        config = app_config.ServiceConfig.get_instance()
        
        # 初始化 MongoDB
        mongo_client = config.get_mongo_client()
        
        # 初始化 MySQL
        mysql_client = config.get_mysql_client()
        
        # 初始化 Redis
        redis_client = config.get_redis_client()
        
        # 初始化 I18n 服務
        i18n_service = config.get_i18n_client()
        
        # 註冊服務
        mongo_repo = MongoDBRepository(mongo_client)
        redis_repo = RedisRepository(redis_client)
        mysql_repo = MySQLRepository(mysql_client)
        
        
        # 註冊服務
        service_registry.ServiceRegistry.register("mongo", mongo_repo)
        service_registry.ServiceRegistry.register("mysql", mysql_repo)
        service_registry.ServiceRegistry.register("redis", redis_repo)
        service_registry.ServiceRegistry.register("i18n", i18n_service)
        