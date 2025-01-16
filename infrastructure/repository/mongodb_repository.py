import os
from typing import Any
import logging
from dotenv import load_dotenv
from domain.interfaces.imongodb_repository import iMongoDBRepository
from application.config.app_config import ServiceConfig
from pymongo import MongoClient

load_dotenv()
dB_name = os.getenv("MONGODB_DB")

class MongoDBRepository(iMongoDBRepository):

    def __init__(self, mongo_client: MongoClient):
        self.client = mongo_client
        self.db = self.client[dB_name]
        self.logger = logging.getLogger('infrastructure')

    def find_by_id(self, collection: str, id: str) -> Any:
        return self.db[collection].find_one({"_id": id})

    def save(self, collection, entity: Any) -> Any:
        return self.db[collection].insert_one(entity)