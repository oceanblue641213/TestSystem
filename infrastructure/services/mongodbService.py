import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

class MongoDBService:
    _instance = None
    
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.max_retry_attempts = 3
        self.retry_delay = 5  # 秒

    def connect(self, uri: str):
        try:
            if not self.is_connected:
                self.client = MongoClient(
                    uri,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000
                )
                # 測試連線
                self.client.admin.command('ping')
                self.is_connected = True
                print("MongoDB connected successfully")
        except Exception as e:
            self.is_connected = False
            print(f"MongoDB connection failed: {e}")
            raise

    def reconnect(self) -> bool:
        """嘗試重新連線"""
        attempts = 0
        while attempts < self.max_retry_attempts:
            try:
                self.client = MongoClient(
                    self.uri,
                    serverSelectionTimeoutMS=5000
                )
                self.client.admin.command('ping')
                self.is_connected = True
                print("MongoDB reconnected successfully")
                return True
            except Exception as e:
                attempts += 1
                print(f"Reconnection attempt {attempts} failed: {e}")
                time.sleep(self.retry_delay)
        return False

    def check_connection(self) -> bool:
        """檢查連線狀態"""
        try:
            self.client.admin.command('ping')
            return True
        except:
            self.is_connected = False
            return False

    def close(self):
        """關閉連線"""
        if self.client:
            self.client.close()
            self.is_connected = False
            print("MongoDB connection closed")