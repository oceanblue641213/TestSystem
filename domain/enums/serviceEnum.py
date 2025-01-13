from enum import Enum

class ServiceType(Enum):
    MYSQL = 'mysql'
    MONGODB = 'mongodb'
    REDIS = 'redis'
    I18N = 'i18n'