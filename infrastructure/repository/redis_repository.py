class RedisRepository:
    def __init__(self, redis_client):
        self.client = redis_client

    def get(self, key: str):
        return self.client.get(key)

    def set(self, key: str, value: str, ex: int = None):
        return self.client.set(key, value, ex=ex)

    def delete(self, key: str):
        return self.client.delete(key)

    # 添加其他你需要的 Redis 操作方法