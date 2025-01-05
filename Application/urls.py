from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from Application.controllers import DISCOVERED_APIS
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 動態生成urlpatterns
urlpatterns = [
    path(f'{key}/', view, name=key)
    for key, view in DISCOVERED_APIS.items()
]

# 添加 Swagger UI 視圖
urlpatterns += [
    # OpenAPI 規範的 URL
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI 視圖
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # JWT 視圖
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]