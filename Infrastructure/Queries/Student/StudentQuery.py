from Domain.entities.student.student import Student
import Domain.dtos.studentDto as dto

class StudentQuery:
    async def Get_Student(data: dto.StudentSerializer) -> str:
        return None