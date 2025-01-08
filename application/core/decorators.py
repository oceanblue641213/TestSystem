from functools import wraps
import logging

logger = logging.getLogger(__name__)

def remove_self_parameter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        if hasattr(result, 'operation'):
            original_operation = result.operation.get_openapi_operation
            
            def new_operation(path: str, method: str) -> dict:
                operation = original_operation(path, method)
                if 'parameters' in operation:
                    operation['parameters'] = [
                        param for param in operation['parameters']
                        if param.get('name') != 'self'
                    ]
                return operation
            
            result.operation.get_openapi_operation = new_operation
        
        return result
    return wrapper