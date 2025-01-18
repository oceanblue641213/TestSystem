import logging
from domain.entities.student.student import Student
from domain.enums.serviceEnum import ServiceType
from application.core.di.container import Container
from application.schemas import ApiResponse

class StudentQuery:
    def __init__(self):
        self.mysql_repo = Container.resolve(ServiceType.MYSQL.value)
        self.logger = logging.getLogger('infrastructure')
        
    async def Get_Specific_Student(self, student_id: str) -> Student:
        try:
            student = await self.mysql_repo.find_by_id_async(Student, student_id)
            
            return student
        except Exception as e:
            self.logger.error(f"Error in get_student_by_id: {str(e)}")
            return ApiResponse(success=False, data=str(e))