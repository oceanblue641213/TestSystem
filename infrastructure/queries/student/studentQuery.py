import logging
from domain.entities.student.student import Student
import domain.dtos.studentDto as dto
from application.config.service_registry import ServiceRegistry
from domain.enums.serviceEnum import ServiceType
from application.schemas import ApiResponse

class StudentQuery:
    def __init__(self):
        self.mysql_repo = ServiceRegistry.get_service(ServiceType.MYSQL)
        self.logger = logging.getLogger('infrastructure')
        
    async def Get_Specific_Student(self, student_id: str) -> Student:
        try:
            student = await self.mysql_repo.find_by_id_async(Student, student_id)
            
            return student
        except Exception as e:
            self.logger.error(f"Error in get_student_by_id: {str(e)}")
            return ApiResponse(success=False, data=str(e))