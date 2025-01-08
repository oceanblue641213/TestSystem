from django.urls import path
from ninja import NinjaAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 創建單一的 NinjaAPI 實例
api = NinjaAPI(
    title="Test System",
    version="1.0.0",
    description="API 文檔",
    docs_url="/docs"
)

# 添加 Swagger UI 視圖
urlpatterns = [
    # Django Ninja API 路由
    path("api/", api.urls),  # 這會包含所有 API 端點和 Ninja 的 Swagger UI
    # JWT 視圖
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# 添加調試端點
@api.get("/debug")
def debug_endpoint(request):
    """測試端點"""
    return {"message": "API is working", "routes": [str(route) for route in api.routes]}