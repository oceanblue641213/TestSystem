from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers as rest_serializers
from functools import wraps

def get_spectacular_type(field_type):
    """
    將 Python 類型映射到 drf_spectacular 類型
    """
    type_mapping = {
        int: 'integer',
        float: 'number',
        str: 'string',
        bool: 'boolean',
        list: 'array',
        dict: 'object'
    }
    return type_mapping.get(field_type, 'string')

def create_dynamic_serializer(dto_class):
    """
    根據 DTO 類動態生成序列化器
    """
    fields = {}
    for field_name, field_type in dto_class.__annotations__.items():
        if field_type == str:
            fields[field_name] = rest_serializers.CharField(required=False)
        elif field_type == int:
            fields[field_name] = rest_serializers.IntegerField(required=False)
        elif field_type == float:
            fields[field_name] = rest_serializers.FloatField(required=False)
        # 可以根據需要擴展更多類型
    
    return type(f'{dto_class.__name__}Serializer', (rest_serializers.Serializer,), fields)

def auto_swagger_and_validate(dto_class, methods=['GET', 'POST']):
    """
    結合方法限制、Swagger 文檔和數據驗證的通用裝飾器
    """
    def decorator(func):
        @wraps(func)
        @extend_schema(
            description=f"API for {dto_class.__name__}",
            parameters=[
                OpenApiParameter(
                    name=field_name, 
                    description=f"{field_name} parameter", 
                    required=False, 
                    location=OpenApiParameter.QUERY,
                    type=get_spectacular_type(field_type)
                ) for field_name, field_type in dto_class.__annotations__.items()
            ],
            request=(
                create_dynamic_serializer(dto_class) if 'POST' in methods or 'PUT' in methods else None
            ),
            responses={200: str, 400: str}  # 預設響應格式，可以根據實際情況調整
        )
        @api_view(methods)
        def wrapper(request, *args, **kwargs):
            # 自動驗證和轉換
            serializer = create_dynamic_serializer(dto_class)(data=request.data)
            if serializer.is_valid():
                dto = dto_class(**serializer.validated_data)
                return func(request, dto, *args, **kwargs)
            return Response(serializer.errors, status=400)
        
        return wrapper
    return decorator
