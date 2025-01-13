from typing import Any
import traceback
import logging

class BaseException(Exception):
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        self.stack_trace = traceback.format_exc()
        logging.error(f"{self.__class__.__name__}: {message}\n{self.stack_trace}")
        super().__init__(self.message)

class BadRequestException(BaseException):
    def __init__(self, message="Bad request"):
        super().__init__(message=message, code=400)
        
class UnauthorizedException(BaseException):
    def __init__(self, message="Unauthorized"):
        super().__init__(message=message, code=401)

class ForbiddenException(BaseException):
    def __init__(self, message="Permission denied"):
        super().__init__(message=message, code=403)

class EntityNotFoundException(BaseException):
    def __init__(self, entity: str, identifier: Any):
        super().__init__(
            message=f"{entity} with id {identifier} not found",
            code=404
        )