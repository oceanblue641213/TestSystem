from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

T = TypeVar('T')

class BaseResponseModel(BaseModel):
    """所有回應 model 的基礎類別"""
    class Config:
        json_encoders = {
            UUID: str,              # UUID 轉字串
            datetime: str,          # datetime 轉字串
        }

class ApiResponse(BaseResponseModel, Generic[T]):
    success: bool
    message: Optional[str] = None  # 用於一般訊息
    error: Optional[str] = None    # 專門用於錯誤訊息
    data: Optional[T] = None