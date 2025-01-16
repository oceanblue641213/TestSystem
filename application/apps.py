import os
from django.apps import AppConfig
from .config import service_registry, app_config
from infrastructure.repository.mongodb_repository import MongoDBRepository
from infrastructure.repository.redis_repository import RedisRepository
from infrastructure.repository.mysql_repository import MySQLRepository
from domain.enums.serviceEnum import ServiceType
from application.core.di.auto_register import auto_register_services
from .registry import auto_import_models

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'

    def ready(self):
        print("MyAppConfig.ready() called")  # 添加日誌
        # 導入 signals
        from . import signals
        
        # 使用新的服務註冊機制
        auto_register_services()
        
        # 使用環境變量來控制
        DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')
        print(f"Current environment: {DJANGO_ENV}")  # 添加日誌
        if DJANGO_ENV == 'development':
            # 只在開發環境執行
            from application.controllers import discover_apis
            discover_apis()
            print("APIs discovered and registered")  # 添加日誌
        
        auto_import_models()

    def initialize_services(self):
        # 獲取配置單例
        config = app_config.ServiceConfig.get_instance()
        
        # 初始化 MySQL
        mysql_client = config.get_mysql_client()
        
        # 初始化 MongoDB
        mongo_client = config.get_mongo_client()
        
        # 初始化 Redis
        # redis_client = config.get_redis_client()
        
        # 初始化 I18n 服務
        # i18n_service = config.get_i18n_client()
        
        # 註冊服務
        mysql_repo = MySQLRepository(mysql_client)
        mongo_repo = MongoDBRepository(mongo_client)
        # redis_repo = RedisRepository(redis_client)
        
        
        # 註冊服務
        service_registry.ServiceRegistry.register(ServiceType.MYSQL, mysql_repo)
        service_registry.ServiceRegistry.register(ServiceType.MONGODB, mongo_repo)
        # service_registry.ServiceRegistry.register(ServiceType.REDIS, redis_repo)
        # service_registry.ServiceRegistry.register(ServiceType.I18N, i18n_service)
        