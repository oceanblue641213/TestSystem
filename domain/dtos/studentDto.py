from dataclasses import dataclass, field
from ninja import Schema

@dataclass
class StudentDto(Schema):
    name: str = field(default="")
    age: int = field(default=0)
    gender: str = field(default="M")