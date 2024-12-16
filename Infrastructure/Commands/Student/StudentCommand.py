from Domain.Entities.Student import Student
import Domain.Dtos.StudentDto as dto

class StudentCommand:
    async def Create_Student(data: dto.StudentSerializer) -> str:
        aaa = data
        serializer = Student.StudentSerializer(data=data)
        if serializer.is_valid():
            student = serializer.save()
            return serializer.data, None
        return None, serializer.errors
    
    async def Update_Student(data: dto.StudentSerializer) -> str:
        return None
    
    async def Delete_Student(id: int) -> str:
        return None