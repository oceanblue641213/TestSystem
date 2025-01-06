from rest_framework import serializers
from typing import TypeVar, Generic, Type
from django.db import models # type: ignore

ModelType = TypeVar('ModelType', bound=models.Model)

class GenericSerializer(Generic[ModelType], serializers.Serializer):
    """
    通用泛型序列化器，支持客製化驗證
    """
    def __init__(self, *args, **kwargs):
        # 允許傳入特定的模型類
        self.model_class = kwargs.pop('model_class', None)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        """
        提供一個可重寫的通用驗證方法
        子類可以覆寫此方法添加特定邏輯
        """
        return data

    def create(self, validated_data):
        """
        通用創建方法
        如果提供了model_class，可以直接創建實例
        """
        if self.model_class:
            return self.model_class.objects.create(**validated_data)
        raise NotImplementedError("未提供model_class")

    def update(self, instance, validated_data):
        """
        通用更新方法
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance