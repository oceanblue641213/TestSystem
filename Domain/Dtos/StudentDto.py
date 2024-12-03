from dataclasses import dataclass, field

@dataclass
class StudentDto():
    Name: str = field(default="")
    Age: int = field(default=0)
    Email: str = field(default="")