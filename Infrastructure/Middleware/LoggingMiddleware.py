import logging
import time

logger = logging.getLogger(__name__)

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 記錄請求開始時間
        start_time = time.time()
        
        # 處理請求
        response = self.get_response(request)
        
        # 計算請求耗時
        duration = time.time() - start_time
        
        # 記錄日誌
        logger.info(
            f"Path: {request.path}, "
            f"Method: {request.method}, "
            f"Status: {response.status_code}, "
            f"Duration: {duration:.2f}s"
        )
        
        return response