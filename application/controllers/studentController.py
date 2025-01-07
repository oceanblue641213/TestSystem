import logging
import asyncio
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from infrastructure.utils.authentication import JWTAuthentication
import domain.dtos.studentDto as dto
import infrastructure.commands.student.studentCommand as cmd
import infrastructure.queries.student.studentQuery as qry
from infrastructure.utils.response import ApiResponse
from application.config.service_registry import ServiceRegistry
from domain.entities.EF.EF import EF as EF

logger = logging.getLogger('your_app')

class StudentAPIView(APIView):
  def __init__(self):
        self.mysql_repo = ServiceRegistry.get_service("mysql")
  permission_classes = [AllowAny]
    
  # 取得學生資料
  # 不需要授權的API

  # @authentication_classes([JWTAuthentication])
  # @permission_classes([IsAuthenticated])
  # @extend_schema(request=dto.StudentSerializer, methods=['GET'])
  def get(self, request, *args, **kwargs):
    try:
      aaa = self.mysql_repo.find_by_id(EF, 'GHG00001')
      # dto = dto.StudentDto(**request.data)
      # await qry.StudentQuery.Get_Student(dto)
      return ApiResponse.success()
    except Exception as e:
      return ApiResponse.error(message=str(e))
  
  # # 創建學生
  # # 需要授權的API
  # @permission_classes([IsAuthenticated])
  # @extend_schema(request=dto.StudentSerializer, methods=['POST'])
  # async def post(self, request, *args, **kwargs):
  #     try:
  #         dto = dto.StudentDto(**request.data)
  #         await cmd.StudentCommand.Create_Student(dto)
  #         return ApiResponse.success()
  #     except Exception as e:
  #         return ApiResponse.error(message=str(e))
  
  # # 更新學生
  # @extend_schema(request=dto.StudentSerializer, methods=['PUT'])
  # async def put(self, request, *args, **kwargs):
  #     try:
  #         dto = dto.StudentDto(**request.data)
  #         await cmd.StudentCommand.Update_Student(dto)
  #         return ApiResponse.success()
  #     except Exception as e:
  #         return ApiResponse.error(message=str(e))
  
  # # 刪除學生
  # @extend_schema(request=dto.StudentSerializer, methods=['DELETE'])
  # async def delete(self, request, *args, **kwargs):
  #     try:
  #         dto = dto.StudentDto(**request.data)
  #         await cmd.StudentCommand.Delete_Student(dto)
  #         return ApiResponse.success()
  #     except Exception as e:
  #         return ApiResponse.error(message=str(e))

# 定義 api_views 字典來註冊 API 視圖
api_views = {
    'student': StudentAPIView.as_view()
}


'''
前端調用流程：
1. 首先通過 `/api/token/` 端點獲取JWT令牌
2. 在後續請求的Authorization header中包含 `Bearer <your_token>`

範例前端請求：
```javascript
// 獲取token
const response = await axios.post('/api/token/', {
  username: 'your_username',
  password: 'your_password'
});
const token = response.data.access;

// 後續API請求
axios.get('/api/protected-endpoint/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
'''