import os
from typing import Any
from dotenv import load_dotenv
from Domain.interfaces import iMongoDB
from Application.config.app_config import ServiceConfig

load_dotenv()
dB_name = os.getenv("MONGODB_DB")

class MongoDBRepository(iMongoDB):

    def __init__(self, collection_name: str):
        self.config = ServiceConfig.get_instance()
        self.db = self.config.get_database()
        self.collection = self.db[collection_name]

    def find_by_id(self, id: str) -> Any:
        return self.collection.find_one({"_id": id})

    def save(self, entity: Any) -> Any:
        return self.collection.insert_one(entity)