import logging
import asyncio
import Infrastructure.Commands.Student.StudentCommand as cmd
import Infrastructure.Queries.Student.StudentQuery as qry
import Domain.Dtos.StudentDto as dto
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from Infrastructure.Utils.Response import ApiResponse

logger = logging.getLogger('your_app')

class StudentAPIView(APIView):
    
    # 取得學生資料
    # 不需要授權的API
    @api_view(['GET'])
    @permission_classes([AllowAny])
    @extend_schema(request=dto.StudentSerializer, methods=['GET'])
    async def get(self, request, *args, **kwargs):
        # 一般日誌
        logger.warning("SPENCER IS HERE")
        # logger.info('使用者登入', extra={
        #     'user_id': 'spencer',
        #     'ip_address': request.META.get('REMOTE_ADDR')
        # })

        # 錯誤日誌
        try:
            # 某些可能出錯的操作
            pass
        except Exception as e:
            logger.error('操作失敗', exc_info=True, extra={
                'user_id': request.user.id
            })
        try:
            dto = dto.StudentDto(**request.data)
            await qry.StudentQuery.Get_Student(dto)
            return ApiResponse.success()
        except Exception as e:
            return ApiResponse.error(message=str(e))
    
    # # 創建學生
    # # 需要授權的API
    # @api_view(['POST'])
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