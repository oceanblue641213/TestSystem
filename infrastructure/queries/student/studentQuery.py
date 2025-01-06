from domain.entities.student.student import Student
import domain.dtos.studentDto as dto

class StudentQuery:
    async def Get_Student(data: dto.StudentSerializer) -> str:
        return None