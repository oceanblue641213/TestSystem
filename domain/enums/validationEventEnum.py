from enum import Enum

class ValidationEvent(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'