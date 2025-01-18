from enum import Enum

class CQRSType(Enum):
    COMMAND = 'Command',
    QUERY = 'Query'