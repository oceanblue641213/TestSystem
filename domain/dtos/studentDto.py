from dataclasses import dataclass, field
from domain.entities.genericSerializer import GenericSerializer
from rest_framework import serializers

@dataclass
class StudentDto():
    name: str = field(default="")
    age: int = field(default=0)
    email: str = field(default="")

class StudentSerializer(GenericSerializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        # 指定模型類
        kwargs['model_class'] = StudentDto
        super().__init__(*args, **kwargs)

    def validate_name(self, value):
        # 客製化用戶名驗證
        if len(value) < 3:
            raise serializers.ValidationError("用戶名太短")
        return value

    def validate(self, data):
        # 可添加跨欄位驗證
        name = data.get('name')
        age = data.get('age')
        email = data.get('email')
        
        # 額外的驗證邏輯
        if StudentDto.objects.filter(name=name).exists():
            raise serializers.ValidationError("用戶名已存在")
        
        return data