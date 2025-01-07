# services/I18nService.py
from typing import Dict, Any, List
from datetime import datetime
from ..helpers.singleton import singleton
from redis import Redis
from pymongo.collection import Collection

@singleton
class I18nService:
    def __init__(
        self,
        mongodb_collection: Collection,
        redis_client: Redis,
        default_lang: str = 'en',
        cache_ttl: int = 3600
    ):
        self.collection = mongodb_collection
        self.redis_client = redis_client
        self.default_lang = default_lang
        self.cache_ttl = cache_ttl

    def _get_translation_key(self, lang: str, key: str) -> str:
        return f"i18n:{lang}:{key}"

    def get_translation(self, key: str, lang: str) -> str:
        redis_key = self._get_translation_key(lang, key)
        
        # 從 Redis 獲取翻譯
        cached_value = self.redis_client.get(redis_key)
        if cached_value:
            return cached_value
        
        # 從 MongoDB 獲取翻譯
        query = {'lang': lang}
        doc = self.collection.find_one(query)
        
        if doc:
            translation_value = doc.get('translations', {}).get(key)
            if translation_value:
                # 存入 Redis
                self.redis_client.set(redis_key, translation_value, ex=self.cache_ttl)
                return translation_value
        
        return key

    def translate_document(self, doc: Dict[str, Any], lang: str) -> Dict[str, Any]:
        result = doc.copy()
        
        for key, value in doc.items():
            if isinstance(value, dict):
                result[key] = self.translate_document(value, lang)
            elif isinstance(value, list):
                result[key] = [
                    self.translate_document(item, lang) if isinstance(item, dict)
                    else item
                    for item in value
                ]
            elif isinstance(value, str):
                result[key] = self.get_translation(key, lang)
                
        return result

    def translate_documents(self, docs: List[Dict[str, Any]], lang: str) -> List[Dict[str, Any]]:
        return [self.translate_document(doc, lang) for doc in docs]

    def refresh_translations(self, lang: str):
        pattern = f"i18n:{lang}:*"
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)