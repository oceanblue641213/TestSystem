from ninja import Schema
from typing import Optional, List, Dict, Any

"""
Args:
    page: 當前頁碼 (默認為1)
    page_size: 每頁筆數 (默認為20)
    filters: 篩選條件字典 (默認為None)
    order_by: 排序欄位，可以是字串或字串列表 (默認為'id')
"""

class SortDto(Schema):
    page: int = 1
    page_size: int = 20
    filters: Optional[Dict[str, Any]] = None
    order_by: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "page_size": 30,
                "filters": {
                    "status": "active",
                    "created_at__gte": "2024-01-01"
                },
                "order_by": ["-created_at", "id"]
            }
        }
""" 
範例用法

page=2,                    # 第二頁
page_size=30,             # 每頁30筆
filters={                  # 篩選條件
    'status': 'active',
    'created_at__gte': '2024-01-01'
},
order_by=['-created_at', 'id'],  # 依建立時間降序，ID升序排序
"""
