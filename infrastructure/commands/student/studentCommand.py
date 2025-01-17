import logging
from domain.entities.student.student import Student
from domain.dtos.studentDto import StudentDto
from domain.events.student.commandEvents import StudentCreated, StudentUpdated, StudentDeleted
from domain.enums.serviceEnum import ServiceType
from application.core.di.container import Container
import domain.exceptions.exceptions as exceptions

class StudentCommand:
    def __init__(self):
        self.mysql_repo = Container.resolve(ServiceType.MYSQL)
        self.logger = logging.getLogger('infrastructure')
    
    async def Create_Student(self, data: StudentDto) -> Student:
        entity = Student(data.name, data.gender, data.age)
    
        # 儲存並返回結果
        saved_student = await self.mysql_repo.save_async(entity)
        return saved_student
    
    async def Update_Student(self, id: str, data: StudentDto) -> Student:
        try:
            # 找不到實體應該要直接回傳 None 或拋出異常
            entity = await self.mysql_repo.find_by_id_async(Student, id)
            if not entity:
                raise exceptions.EntityNotFoundError(f"Student with id {id} not found")
            
            # 觸發領域事件
            event = StudentUpdated(data.name, data.gender, data.age)
            entity.TriggerUpdated(event)
            
            # 儲存並返回更新後的實體
            return await self.mysql_repo.save_async(entity)
        except Exception as e:
            self.logger.error(f"Error updating student: {str(e)}")
            raise
    
    async def Delete_Student(self, id: int) -> str:
        try:
            entity = await self.mysql_repo.find_by_id_async(Student, id)
            if not entity:
                raise exceptions.EntityNotFoundError(f"Student with id {id} not found")
            
            # 觸發領域事件
            entity.TriggerDeleted(StudentDeleted())
            
            # 儲存並返回更新後的實體
            return await self.mysql_repo.save_async(entity)
        except Exception as e:
            self.logger.error(f"Error deleting student: {str(e)}")
            raise