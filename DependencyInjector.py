class DependencyInjector:
    def __init__(self):
        # 服務註冊表，用於存儲所有的服務及其實例
        self._services = {}

    def register(self, service, instance=None, factory=None):
        """
        註冊一個服務，通過實例或工廠函數來注入服務。
        :param service: 服務名稱或類型
        :param instance: 服務實例
        :param factory: 可選的工廠函數，用於創建服務實例
        """
        if instance:
            self._services[service] = instance
        elif factory:
            self._services[service] = factory
        else:
            raise ValueError("You must provide either an instance or a factory function.")

    def resolve(self, service):
        """
        解決並返回服務實例。
        如果服務是以工廠方式註冊，會調用工廠函數來創建實例。
        """
        if service in self._services:
            value = self._services[service]
            if callable(value):  # 如果是工廠函數，則調用它來獲取實例
                return value()
            return value
        else:
            raise ValueError(f"Service '{service}' not found.")
