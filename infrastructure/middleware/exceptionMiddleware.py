from rest_framework.views import exception_handler
from rest_framework.response import Response
from domain.exceptions.exceptions import BaseException
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

def custom_exception_handler(exc, context):
    # 先處理自定義異常
    if isinstance(exc, BaseException):
        return Response(
            {
                "success": False,
                "message": exc.message,
                "code": exc.code,
                "errors": getattr(exc, 'errors', None)
            },
            status=exc.code
        )
    
    # 處理 Django 的 ValidationError
    if isinstance(exc, DjangoValidationError):
        return Response(
            {
                "success": False,
                "message": "Validation Error",
                "code": 400,
                "errors": exc.message_dict if hasattr(exc, 'message_dict') else str(exc)
            },
            status=400
        )

    # 處理 DRF 的 ValidationError
    if isinstance(exc, DRFValidationError):
        return Response(
            {
                "success": False,
                "message": "Validation Error",
                "code": 400,
                "errors": exc.detail
            },
            status=400
        )

    # 使用 DRF 預設的例外處理
    response = exception_handler(exc, context)
    
    # 如果 DRF 也沒處理到的例外
    if response is None:
        return Response(
            {
                "success": False,
                "message": str(exc),
                "code": 500,
                "errors": None
            },
            status=500
        )

    return response