from Domain.Entities.Student import Student
import Domain.Dtos.StudentDto as dto

class StudentQuery:
    async def Get_Student(data: dto.StudentSerializer) -> str:
        return None