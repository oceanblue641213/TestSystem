import os
from typing import Optional
from functools import lru_cache
import logging
from django.conf import settings
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()
mongodb_url = os.getenv("MONGODB_URL")

class ServiceConfig:
    _instance: Optional['ServiceConfig'] = None
    
    def __init__(self):
        if ServiceConfig._instance is not None:
            raise Exception("ServiceConfig is a singleton!")
        self.initialize_services()
    
    @classmethod
    def get_instance(cls) -> 'ServiceConfig':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def initialize_services(self):
        # 初始化各種服務
        self.mongo_client = None
        self.redis_client = None
        self.mysql_client = None
        # 其他服務初始化...

    @lru_cache
    def get_mongo_client(self) -> MongoClient:
        """
        獲取 MongoDB 客戶端連接
        如果連接不存在則創建新連接
        """
        if not self.mongo_client:
            try:
                # 創建客戶端連接
                self._mongo_client = MongoClient(
                    mongodb_url,
                    serverSelectionTimeoutMS=5000  # 5秒超時
                )
                
                # 測試連接
                self._mongo_client.admin.command('ping')
                logger.info("Successfully connected to MongoDB")
                
            except ConnectionFailure as e:
                logger.error(f"MongoDB Connection failed: {str(e)}")
                raise

        return self.mongo_client
        
    @lru_cache
    def get_redis_client(self):
        if not self.redis_client:
            # 初始化 redis 連接
            pass
        return self.redis_client
        
    @lru_cache
    def get_mysql_client(self):
        if not self.mysql_client:
            # 初始化 mysql 連接
            pass
        return self.mysql_client
    
    def get_mongo_database(self, db_name: str = None):
        """
        獲取指定的MongoDB數據庫實例
        """
        client = self.get_mongo_client()
        return client[db_name or settings.MONGODB_DB]