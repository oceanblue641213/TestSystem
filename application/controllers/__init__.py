import os
import importlib
from pathlib import Path
from application.urls import api

def discover_apis():
    controllers_dir = Path(__file__).parent
    
    for file in controllers_dir.glob('*.py'):
        if file.name == '__init__.py':
            continue
            
        module_name = f"application.controllers.{file.stem}"
        
        try:
            module = importlib.import_module(module_name)
            
            # 檢查模組是否有 router 屬性
            if hasattr(module, 'router'):
                # 從文件名獲取前綴
                prefix = file.stem.lower().replace('controller', '')
                # 註冊路由器，使用文件名作為前綴
                api.add_router(f"/{prefix}/", module.router)
        except Exception as e:
            print(f"Error loading {module_name}: {str(e)}")
            import traceback
            print(traceback.format_exc())
