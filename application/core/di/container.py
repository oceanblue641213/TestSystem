from typing import Dict, Type, Any
from application.config.app_config import ServiceConfig
from application.config.service_registry import ServiceRegistry
from domain.enums.serviceEnum import ServiceType
from infrastructure.repository.mongodb_repository import MongoDBRepository
from infrastructure.repository.redis_repository import RedisRepository
from infrastructure.repository.mysql_repository import MySQLRepository

class Container:
    _instance = None
    _services: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Container, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, name: str, service: Any):
        """註冊服務到容器"""
        cls._services[name] = service

    @classmethod
    def resolve(cls, name: str) -> Any:
        """從容器中解析服務"""
        return cls._services.get(name)

    @classmethod
    def initialize_core_services(cls):
        # 獲取 ServiceConfig 單例
        config = ServiceConfig.get_instance()
        
        # 初始化核心服務
        mysql_client = config.get_mysql_client()
        redis_client = config.get_redis_client()
        # mongo_client = config.get_mongo_client()
        # i18n_service = config.get_i18n_client()
        
        # 創建 repositories
        mysql_repo = MySQLRepository(mysql_client)
        # mongo_repo = MongoDBRepository(mongo_client)
        
        # 註冊到 ServiceRegistry
        ServiceRegistry.register(ServiceType.MYSQL.value, mysql_repo)
        ServiceRegistry.register(ServiceType.REDIS.value, redis_client)
        # ServiceRegistry.register(ServiceType.MONGODB, mongo_repo)
        
        # 同時也註冊到容器（用於新的依賴注入機制）
        cls.register(ServiceType.MYSQL.value, mysql_repo)
        cls.register(ServiceType.REDIS.value, redis_client)
        # cls.register('mongo', mongo_repo)