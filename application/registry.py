import os
import logging
import importlib
from pathlib import Path
from django.conf import settings

# 設置 logger
logger = logging.getLogger(__name__)

def auto_import_models():
    try:
        # 獲取 entities 目錄的路徑
        entities_path = Path(__file__).parent.parent / 'domain' / 'entities'
        
        if not entities_path.exists():
            raise FileNotFoundError(f"Entities directory not found at {entities_path}")
            
        logger.info(f"Starting model import from {entities_path}")
        
        # 遍歷所有 .py 文件
        for file in entities_path.glob('*.py'):
            if file.stem == '__init__':
                continue
                
            try:
                # 將檔案路徑轉換為模組路徑
                module_path = f"domain.entities.{file.stem}"
                
                # 導入模組
                module = importlib.import_module(module_path)
                
                # 在開發環境輸出調試信息
                if settings.DEBUG:
                    logger.debug(f"Successfully imported {module_path}")
                    # 輸出該模組中定義的所有 models
                    from django.db import models
                    model_classes = [cls for cls in module.__dict__.values() 
                                  if isinstance(cls, type) 
                                  and issubclass(cls, models.Model) 
                                  and cls.__module__ == module.__name__]
                    for model in model_classes:
                        logger.debug(f"Found model: {model.__name__}")
                
            except ImportError as e:
                logger.error(f"Failed to import {file.name}: {str(e)}")
                if settings.DEBUG:
                    raise  # 在開發環境中立即報錯
                continue  # 在生產環境中繼續處理其他文件
                
    except Exception as e:
        logger.error(f"Error during model auto-import: {str(e)}")
        if settings.DEBUG:
            raise