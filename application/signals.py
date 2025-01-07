from django.core.signals import request_finished
from django.db import connection
from django.dispatch import receiver
from application.config.app_config import ServiceConfig

@receiver(request_finished)
def handle_request_finished(sender, **kwargs):
    """在每個請求結束後檢查連線狀態"""
    config = ServiceConfig.get_instance()
    config.check_connections()