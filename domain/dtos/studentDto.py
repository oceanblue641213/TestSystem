from dataclasses import dataclass, field
from ninja import Schema

@dataclass
class StudentDto(Schema):
    name: str = field(default="")
    age: int = field(default=0)
    email: str = field(default="")