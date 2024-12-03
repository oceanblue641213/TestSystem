from django.http import JsonResponse
from functools import wraps

def api_method_required(methods):
    """
    限制API的調用方法
    
    :param methods: 允許的HTTP方法列表，如 ['GET', 'POST']
    :return: 裝飾器
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # 檢查請求方法是否在允許的方法列表中
            if request.method not in methods:
                return JsonResponse({
                    'error': 'Method Not Allowed',
                    'allowed_methods': methods
                }, status=405)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator