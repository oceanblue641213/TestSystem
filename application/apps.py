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
        # 導入 signals
        from . import signals
        
        # 使用新的服務註冊機制
        auto_register_services()
        
        # 使用環境變量來控制
        DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')
        if DJANGO_ENV == 'development':
            # 只在開發環境執行
            from application.controllers import discover_apis
            discover_apis()
        
        auto_import_models()
        