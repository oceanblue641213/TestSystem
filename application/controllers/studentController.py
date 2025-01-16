import logging
from application.core.decorators import remove_self_parameter
from ninja import Router
from django.http import HttpRequest
from domain.dtos.studentDto import StudentDto
from infrastructure.queries.student.studentQuery import StudentQuery
from infrastructure.commands.student.studentCommand import StudentCommand
from typing import Any
from application.schemas import ApiResponse
from application.config.service_registry import ServiceRegistry
from ninja.security import HttpBearer
from application.auth.jwt_auth import JWTAuth
from domain.enums.serviceEnum import ServiceType
from application.core.di.container import Container

router = Router(tags=["students"])
logger = logging.getLogger('application')

class StudentController:
    def __init__(self):
        self.mysql_repo = ServiceRegistry.get_service(ServiceType.MYSQL)
    # 在類定義時就初始化服務
    command = Container.resolve('StudentCommand')
    query = Container.resolve('StudentQuery')
        
    @remove_self_parameter
    @router.get("/", summary="Get all students", response=ApiResponse[str])
    async def get_student(request: HttpRequest) -> Any:
        try:
            # 假設 mysql_repo 已經支援非同步操作
            return ApiResponse(success=True, data="123")
        except Exception as e:
            logger.error(f"Error in get_students: {str(e)}")
            return ApiResponse(success=False, data=str(e))

    # @remove_self_parameter
    @router.get("/{student_id}", summary="Get student by ID", auth=JWTAuth())
    async def get_student_by_id(request: HttpRequest, student_id: str) -> Any:
        try:
            student = StudentQuery.Get_Specific_Student(student_id)
            if not student:
                return ApiResponse.error(message="Student not found", status=404)
            return ApiResponse(success=True, data="123")
        except Exception as e:
            logger.error(f"Error in get_student_by_id: {str(e)}")
            return ApiResponse(success=False, data=str(e))

    # @remove_self_parameter
    @router.post("/", response=ApiResponse[StudentDto])
    async def create_student(request: HttpRequest, student: StudentDto) -> Any:
        try:
            await StudentController.command.Create_Student(student)
            
            return ApiResponse(success=True, data=student)
        except Exception as e:
            print(f"Error in create_student: {str(e)}")
            return ApiResponse(success=False, data=str(e))

# 直接導出 router
__all__ = ['router']


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