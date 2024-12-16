from rest_framework.views import exception_handler
from Infrastructure.Utils.Response import ApiResponse
from Domain.Exceptions.Exceptions import BusinessLogicException

def custom_exception_handler(exc, context):
    # 處理自定義異常
    if isinstance(exc, BusinessLogicException):
        return ApiResponse.error(
            message=exc.message, 
            status_code=exc.error_code
        )
    
    # 使用DRF默認異常處理
    return exception_handler(exc, context)