class ServiceRegistry:
    """服務註冊管理器"""
    _services = {}
    
    @classmethod
    def register(cls, service_name: str, service_instance):
        cls._services[service_name] = service_instance
    
    @classmethod
    def get_service(cls, service_name: str):
        return cls._services.get(service_name)