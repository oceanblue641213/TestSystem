class BusinessLogicException(Exception):
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ResourceNotFoundException(BusinessLogicException):
    def __init__(self, resource_name):
        super().__init__(f"{resource_name} not found", 404)