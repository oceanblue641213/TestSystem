# from injector import Module, singleton
# # from Infrastructure.Commands.Service import MyService

# class AppModule(Module):
#      def configure(self, binder):
#         # 使用singleton方式綁定服務
#         # binder.bind(MyService, to=MyService, scope=singleton)
#         print()

from django.db import connection
from django.http import JsonResponse
from Infrastructure.Utils.Decorator import api_method_required

#region 測試
@api_method_required(['GET'])
def api_user_list(request):
    # 處理獲取用戶列表的邏輯
    print("測試開始")
    # print(request.GET.get('id'))
    try:
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT * FROM GWP")
        #     result = cursor.fetchone()
        #     print(f"查詢結果: {result}")
        return JsonResponse({
        "status": "success",
        "users": [
            {"id": 1, "name": "John"}
        ]
    })
    except Exception as e:
        print(f"連線或查詢失敗: {e}")
        return JsonResponse({
        "status": "failure",
        "users": [
            {"id": 2, "name": "Jane"}
        ]
    })
#endregion

def api_create_user(request):
    # 處理創建用戶的邏輯
    return JsonResponse({
        "status": "success",
        "message": "User created"
    })

# Application/Controllers/ProductController.py
def api_get_product_list(request):
    # 處理獲取產品列表的邏輯
    return JsonResponse({
        "status": "success", 
        "products": [
            {"id": 1, "name": "Product A"},
            {"id": 2, "name": "Product B"}
        ]
    })