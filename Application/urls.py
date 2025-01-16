from django.urls import path
from ninja import NinjaAPI
from application.api import api
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 添加 Swagger UI 視圖
urlpatterns = [
    # Django Ninja API 路由
    path("api/", api.urls),  # 這會包含所有 API 端點和 Ninja 的 Swagger UI
    # JWT 視圖
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]