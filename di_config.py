from injector import Injector
# from .Infrastructure.di_modules import CoreModule

# 集中管理所有依賴注入模組
def create_injector():
    return Injector([
        # CoreModule()
    ])

# 全局注入器
global_injector = create_injector()