from dataclasses import dataclass
from datetime import datetime

@dataclass
class BaseEvent:
    occurred_on: datetime = datetime.now()