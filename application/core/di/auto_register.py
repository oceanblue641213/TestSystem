import os
import importlib
from pathlib import Path
from django.apps import apps
from .container import Container

def auto_register_services():
    # 1. 初始化核心服務（數據庫連接等）
    Container.initialize_core_services()
    
    # 2. 尋找 infrastructure 目錄下的 commands 和 queries
    infrastructure_path = Path(__file__).parent.parent.parent.parent / 'infrastructure'  # 調整路徑到 infrastructure 目錄
    
    commands_path = infrastructure_path / 'commands'
    if commands_path.exists():
        register_modules_in_directory(commands_path, 'commands')
    
    queries_path = infrastructure_path / 'queries'
    if queries_path.exists():
        register_modules_in_directory(queries_path, 'queries')

def register_modules_in_directory(base_dir: Path, module_type: str):
    # 遍歷所有子目錄
    for category_dir in base_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith('__'):
            continue
            
        # 遍歷子目錄中的所有 .py 文件
        for file in category_dir.glob('*.py'):
            if file.name.startswith('__'):
                continue
                
            # 構建模組路徑，例如 "infrastructure.commands.student.studentCommand"
            module_path = f"infrastructure.{module_type}.{category_dir.name}.{file.stem}"
            
            try:
                module = importlib.import_module(module_path)
                
                # 檢查模組中的所有屬性
                for attr_name in dir(module):
                    if attr_name.endswith(module_type.capitalize()[:-1]):  # Command 或 Query
                        service_class = getattr(module, attr_name)
                        service_instance = service_class()
                        Container.register(attr_name, service_instance)
                        print(f"Registered service: {attr_name}")  # 可以加入日誌
                        
            except ImportError as e:
                print(f"Error importing module {module_path}: {str(e)}")
                continue