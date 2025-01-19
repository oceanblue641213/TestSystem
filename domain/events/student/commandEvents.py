from dataclasses import dataclass

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
    pass