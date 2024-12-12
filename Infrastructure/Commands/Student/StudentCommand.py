from Domain.Entities.Students import Student
import Domain.Dtos.StudentDto as dto

class StudentCommand:
    def Create_Student(data):
        aaa = data
        serializer = Student.StudentSerializer(data=data)
        if serializer.is_valid():
            student = serializer.save()
            return serializer.data, None
        return None, serializer.errors