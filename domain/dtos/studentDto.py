from dataclasses import dataclass, field
from ninja import Schema
from domain.dtos.sortDto import SortDto

class StudentDto(Schema):
    name: str = ""
    age: int = 0
    gender: str = "M"

    class Config:
        from_attributes = True
    
class StudentDto2(Schema):
    id: str = ""
    name: str = ""
    create_date: str = ""

    class Config:
        from_attributes = True

"""
class Config:
    from_attributes = True

這個設置告訴 Pydantic：

允許從物件的屬性讀取數據（使用 getattr）
不僅僅限於字典形式的數據輸入
特別適用於 ORM 模型轉 DTO 的場景
"""