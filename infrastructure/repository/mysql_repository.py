from django.db import connection
from django.db.models import Model
from typing import List, Optional, Type
from domain.interfaces.imysql_repository import iMySQLRepository

class MySQLRepository(iMySQLRepository):
    def __init__(self, connection):
        self.connection = connection

    def find_all(self, model: Type[Model]) -> List[Model]:
        return model.objects.all()

    def find_by_id(self, model: Type[Model], id: str) -> Optional[Model]:
        try:
            return model.objects.get(Id=id)
        except model.DoesNotExist:
            return None

    def find_by_filter(self, model: Type[Model], **kwargs) -> List[Model]:
        return model.objects.filter(**kwargs)

    def create(self, model: Type[Model], data: dict) -> Model:
        return model.objects.create(**data)

    def update(self, instance: Model, data: dict) -> Model:
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: Model) -> bool:
        instance.delete()
        return True