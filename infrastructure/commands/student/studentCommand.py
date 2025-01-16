import logging
from domain.entities.student.student import Student
from domain.dtos.studentDto import StudentDto
from domain.events.student.commandEvents import StudentCreated, StudentUpdated, StudentDeleted
from domain.enums.serviceEnum import ServiceType
from application.core.di.container import Container

class StudentCommand:
    def __init__(self):
        self.mysql_repo = Container.resolve(ServiceType.MYSQL)
        self.logger = logging.getLogger('infrastructure')
    
    async def Create_Student(self, data: StudentDto) -> str:
        event = StudentCreated(data.name, data.gender, data.age)
        Student.TriggerCreated(event)
        
        await self.mysql_repo.save_async(Student)
        return None
    
    async def Update_Student(self, data: StudentDto) -> str:
        event = StudentUpdated(data.name, data.gender, data.age)
        Student.TriggerUpdated(event)
        
        await self.mysql_repo.save_async(Student)
        return None
    
    async def Delete_Student(self, id: int) -> str:
        event = StudentDeleted()
        Student.TriggerUpdated
        return None