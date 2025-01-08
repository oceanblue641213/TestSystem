from functools import wraps
from ninja import Router

def remove_self_param(original_route):
    @wraps(original_route)
    def wrapper(*args, **kwargs):
        route = original_route(*args, **kwargs)
        original_operation = route.operation.get_openapi_operation
        
        def new_operation(path: str, method: str) -> dict:
            operation = original_operation(path, method)
            print("Original operation:", operation)
            if 'parameters' in operation:
                operation['parameters'] = [
                    param for param in operation['parameters']
                    if param.get('name') != 'self'
                ]
            return operation
            
        route.operation.get_openapi_operation = new_operation
        return route
    return wrapper

class CustomRouter(Router):
    def __init__(self, *args, **kwargs):
        self.router_tags = kwargs.get('tags', [])  # 保存 tags
        # 確保所有參數都正確傳遞給父類
        super().__init__(*args, **kwargs)

    def _apply_decorator(self, method):
        @wraps(method)
        def decorated(*args, **kwargs):
            # 確保 tags 被正確設置
            if 'tags' not in kwargs and self.router_tags:
                kwargs['tags'] = self.router_tags
            route = method(*args, **kwargs)
            return remove_self_param(route)
        return decorated

    def get(self, *args, **kwargs):
        return self._apply_decorator(super().get(*args, **kwargs))
    
    def post(self, *args, **kwargs):
        return self._apply_decorator(super().post(*args, **kwargs))
    
    def put(self, *args, **kwargs):
        return self._apply_decorator(super().put(*args, **kwargs))
    
    def delete(self, *args, **kwargs):
        return self._apply_decorator(super().delete(*args, **kwargs))