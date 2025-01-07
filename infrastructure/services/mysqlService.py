from django.db import connections, connection
from django.db.utils import OperationalError
from django.conf import settings
import time

class MySQLService:
    _instance = None

    def __init__(self):
        self.is_connected = False
        self.max_retry_attempts = 3
        self.retry_delay = 5
        # 從 Django settings 獲取資料庫配置
        self.db_settings = settings.DATABASES['default']

    def connect(self):
        try:
            if not self.is_connected:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                self.is_connected = True
                print("MySQL connected successfully")
        except Exception as e:
            self.is_connected = False
            print(f"MySQL connection failed: {e}")
            raise

    def reconnect(self) -> bool:
        """嘗試重新連線"""
        attempts = 0
        while attempts < self.max_retry_attempts:
            try:
                connections.close_all()  # 關閉所有連線
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                self.is_connected = True
                print("MySQL reconnected successfully")
                return True
            except Exception as e:
                attempts += 1
                print(f"Reconnection attempt {attempts} failed: {e}")
                time.sleep(self.retry_delay)
        return False

    def check_connection(self) -> bool:
        """檢查連線狀態"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except OperationalError:
            self.is_connected = False
            return False

    def close(self):
        """關閉所有連線"""
        connections.close_all()
        self.is_connected = False
        print("MySQL connections closed")