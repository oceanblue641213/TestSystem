import os
from typing import Optional
from functools import lru_cache
import redis
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from infrastructure.services.i18nService import I18nService
from infrastructure.services.mysqlService import MySQLService
from infrastructure.services.mongodbService import MongoDBService
from django.db import connection

load_dotenv()
mongodb_url = os.getenv("MONGODB_URL")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")
translate_collection = os.getenv("TRANSLATE_COLLECTION")

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
        self.i18n_client = None
        self.mysql_service = None
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
                self.mongo_service = MongoDBService()
                self.mongo_service.connect(mongodb_url)
                # 將 mongo_service 的 client 賦值給 mongo_client
                self.mongo_client = self.mongo_service.client
                # logger.info("Successfully connected to MongoDB")
                
            except ConnectionFailure as e:
                # logger.error(f"MongoDB Connection failed: {str(e)}")
                raise

        return self.mongo_client
        
    @lru_cache
    def get_redis_client(self):
        if not self.redis_client:
            try:
                self.redis_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    password=redis_password,
                    db=0,
                    decode_responses=True
                )
                # 嘗試連接 Redis
                self.redis_client.ping()
                print("Redis connection successful")
            except Exception as e:
                print(f"Error connecting to Redis: {e}")
                raise
            
        return self.redis_client
    
    def get_i18n_client(self):
        if not self.i18n_client:
            try:
                # 初始化 i18n 連接
                self.i18n_client = I18nService(
                mongodb_collection=self.mongo_client[translate_collection],
                redis_client=self.redis_client,
                default_lang='en',
                cache_ttl=3600
                )
            except Exception as e:
                print(f"Error connecting to i18n: {e}")
                raise
            
        return self.i18n_client
        
    @lru_cache
    def get_mysql_client(self):
        try:
            # 測試連線
            self.mysql_service = MySQLService()
            self.mysql_service.connect()
            print("MySQL connection successful")
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            raise
        
        return connection

    def cleanup(self):
        """清理所有資源"""
        # if self.mongo_service:
        #     self.mongo_service.close()
        if self.mysql_service:
            self.mysql_service.close()

    def check_connections(self):
        """檢查所有連線狀態"""
        # mongo_ok = self.mongo_service.check_connection()
        mysql_ok = self.mysql_service.check_connection()
        
        # 如果有連線斷開，嘗試重新連線
        # if not mongo_ok:
        #     self.mongo_service.reconnect()
        if not mysql_ok:
            self.mysql_service.reconnect()