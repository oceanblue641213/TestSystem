import os
import importlib
import inspect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

def auto_discover_apis():
    apis = {}
    current_dir = os.path.dirname(__file__)
    
    # 遍歷當前目錄下的所有Python文件
    for filename in os.listdir(current_dir):
        if filename.endswith('Controller.py') and filename != '__init__.py':
            module_name = f'Application.Controllers.{filename[:-3]}'
            module = importlib.import_module(module_name)
            
            # 檢查模塊中是否有 api_views 屬性（可能是基於類的視圖）
            if hasattr(module, 'api_views'):
                for key, view in module.api_views.items():
                    # 若視圖是基於 APIView 類別
                    if isinstance(view, APIView):
                        # 自動包裝為 csrf_exempt 和 http 方法裝飾器
                        wrapped_view = csrf_exempt(require_http_methods(["GET", "POST", "PUT", "DELETE"])(view))
                        apis[key] = wrapped_view
                    else:
                        apis[key] = view  # 其他情況視為普通函數視圖
    
    return apis

# 自動收集所有API
DISCOVERED_APIS = auto_discover_apis()