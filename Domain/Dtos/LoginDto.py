from dataclasses import dataclass, field
from Domain.Entities.GenericSerializer import GenericSerializer
from rest_framework import serializers

@dataclass
class LoginDto():
    username: str = field(default="")
    password: str = field(default="")