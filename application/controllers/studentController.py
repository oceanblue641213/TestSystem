import logging
from ninja import Router
from django.http import HttpRequest
from domain.dtos.studentDto import StudentDto
from typing import Any
from application.schemas import ApiResponse
from ninja.security import HttpBearer
from application.auth.jwt_auth import JWTAuth
from application.core.di.container import Container

router = Router(tags=["students"])
logger = logging.getLogger('application')

class StudentController:
    
    # 在類定義時就初始化服務
    command = Container.resolve('StudentCommand')
    query = Container.resolve('StudentQuery')
        
    @router.get("/", summary="Get all students", response=ApiResponse[str])
    async def get_student(request: HttpRequest) -> Any:
        try:
            # 假設 mysql_repo 已經支援非同步操作
            return ApiResponse(success=True, data="123")
        except Exception as e:
            logger.error(f"Error in get_students: {str(e)}")
            return ApiResponse(success=False, data=str(e))

    @router.get("/{student_id}", summary="Get student by ID", auth=JWTAuth())
    async def get_student_by_id(request: HttpRequest, student_id: str) -> Any:
        try:
            
            return ApiResponse(success=True, data="123")
        except Exception as e:
            logger.error(f"Error in get_student_by_id: {str(e)}")
            return ApiResponse(success=False, data=str(e))

    @router.post("/", response=ApiResponse[StudentDto])
    async def create_student(request: HttpRequest, student: StudentDto) -> Any:
        try:
            created_student = await StudentController.command.Create_Student(student)
            
            return ApiResponse(success=True, data=created_student)
        except Exception as e:
            # 建議使用logger而不是print
            logger.error(f"Error in create_student: {str(e)}")
            # 建議返回更具體的錯誤訊息
            return ApiResponse(success=False, error=str(e))
    
    @router.put("/{student_id}", response=ApiResponse[StudentDto])
    async def update_student(request: HttpRequest, student_id: str, data: StudentDto) -> ApiResponse:
        try:
            updated_student = await StudentController.command.Update_Student(student_id, data)
            if not updated_student:
                return ApiResponse(
                    success=False,
                    error="Student not found"
                )
            return ApiResponse(
                success=True,
                data=updated_student
            )
        except Exception as e:
            return ApiResponse(
                success=False,
                error=str(e)
            )

    @router.delete("/{student_id}", response=ApiResponse[bool])
    async def delete_student(request: HttpRequest, student_id: str) -> ApiResponse:
        try:
            result = await StudentController.command.Delete_Student(student_id)
            return ApiResponse(
                success=result,
                message="Student deleted successfully" if result else "Student not found"
            )
        except Exception as e:
            return ApiResponse(
                success=False,
                error=str(e)
            )

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