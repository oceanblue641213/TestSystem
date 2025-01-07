import os
import importlib
from pathlib import Path

DISCOVERED_APIS = {}

def discover_apis():
    # 獲取 controllers 目錄的路徑
    controllers_dir = Path(__file__).parent
    
    # 遍歷所有 .py 文件
    for file in controllers_dir.glob('*.py'):
        if file.name == '__init__.py':
            continue
            
        # 將檔案路徑轉換為模組路徑
        module_name = f"application.controllers.{file.stem}"
        
        try:
            module = importlib.import_module(module_name)
            
            if hasattr(module, 'api_views'):
                DISCOVERED_APIS.update(module.api_views)
        except Exception as e:
            print(f"Error loading {module_name}: {str(e)}")
            print(f"Error type: {type(e)}")  # 添加錯誤類型
            import traceback
            print(traceback.format_exc())  # 添加完整堆疊追踪

# 執行 API 發現
discover_apis()

# 導出 DISCOVERED_APIS
__all__ = ['DISCOVERED_APIS']