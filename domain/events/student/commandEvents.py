from uuid import UUID
from dataclasses import dataclass, field
from domain.events.baseEvent import BaseEvent

@dataclass
class StudentCreated():
    name: str
    age: int
    gender: str

@dataclass
class StudentUpdated():
    name: str
    age: int
    gender: str

@dataclass
class StudentDeleted():
    student_id: UUID