import os
from typing import Any
from dotenv import load_dotenv
from Domain.interfaces.iMongoDB import iMongoDB
from Application.config.app_config import ServiceConfig

load_dotenv()
dB_name = os.getenv("MONGODB_DB")

class MongoDBRepository(iMongoDB):

    def __init__(self):
        self.config = ServiceConfig.get_instance()
        self.db = self.config.get_mongo_database(dB_name)

    def find_by_id(self, collection: str, id: str) -> Any:
        return self.db[collection].find_one({"_id": id})

    def save(self, collection, entity: Any) -> Any:
        return self.db[collection].insert_one(entity)