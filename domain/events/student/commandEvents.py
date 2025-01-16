from dataclasses import dataclass, field

class StudentCreated:
    def __init__(self, name: str, gender: str, age: int):
        self.name = name
        self.gender = gender
        self.age = age
    
    name: str
    age: int
    email: str

class StudentUpdated:
    name: str
    age: int
    email: str

class StudentDeleted:
    pass