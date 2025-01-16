from ninja import NinjaAPI

# 創建單一的 NinjaAPI 實例
api = NinjaAPI(
    title="Test System",
    version="1.0.0",
    description="API 文檔",
    docs_url="/docs"
)

# 添加調試端點
@api.get("/debug")
def debug_endpoint(request):
    """測試端點"""
    return {
        "message": "API is working",
        "total_routes": len(api.urls),
        "routes": [
            {
                "path": route.path,
                "methods": list(route.methods),
                "tags": route.tags if hasattr(route, 'tags') else None
            }
            for route in api.routes
        ]
    }