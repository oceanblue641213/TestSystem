from Domain.Entities.Students import Student

student = Student(name="Alice", age=20, email="alice@example.com")

# 使用方法
print(student.get_full_info())
print(student.is_adult())

def GetStudentAge(id):
    print()