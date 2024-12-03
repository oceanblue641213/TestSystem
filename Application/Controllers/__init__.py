import os
import importlib
import inspect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def auto_discover_apis():
    apis = {}
    current_dir = os.path.dirname(__file__)
    
    # 遍歷當前目錄下的所有Python文件
    for filename in os.listdir(current_dir):
        if filename.endswith('Controller.py') and filename != '__init__.py':
            module_name = f'Application.Controllers.{filename[:-3]}'
            module = importlib.import_module(module_name)
            
            # 找出所有以api開頭的函數
            for name, func in inspect.getmembers(module):
                if name.startswith('api_') and callable(func):
                    # 默認添加csrf_exempt和http方法裝飾器
                    wrapped_func = csrf_exempt(require_http_methods(["GET", "POST", "PUT", "DELETE"])(func))
                    apis[f'{filename[:-13].lower()}/{name[4:]}'] = wrapped_func
    
    return apis

# 自動收集所有API
DISCOVERED_APIS = auto_discover_apis()