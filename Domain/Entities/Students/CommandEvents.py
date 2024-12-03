from Domain.Dtos.StudentDto import StudentDto

class StudentCreate:
    def __init__(self, std: StudentDto):
        self._Name = std.Name
        self._Age = std.Age
        self._Email = std.Email

        # 可能還有一些其他要傳入Entity去處理的property，會在這邊一併附上

    @property
    def name(self):
        return self._Name
    
    @name.setter
    def name(self, value):
        self._Name = value
    
    @property
    def age(self):
        return self._Age
    
    @age.setter
    def age(self, value):
        self._Age = value
    
    @property
    def email(self):
        return self._Email
    
    @email.setter
    def email(self, value):
        self._Email = value