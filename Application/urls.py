from django.urls import path
from Application.Controllers import DISCOVERED_APIS
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from Application.Controllers import DISCOVERED_APIS

# 動態生成urlpatterns
urlpatterns = [
    path(f'{key}/', view, name=key)
    for key, view in DISCOVERED_APIS.items()
]

# 添加 Swagger UI 視圖
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns += [
    # OpenAPI 規範的 URL
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI 視圖
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]