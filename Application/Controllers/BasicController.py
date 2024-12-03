from django.db import connection
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StudentAPIView(APIView):
    def get(self, request):
        # with connection.cursor() as cursor:
            #     cursor.execute("SELECT * FROM GWP")
            #     result = cursor.fetchone()
            #     print(f"查詢結果: {result}")
        return Response({"message": "This is the get Student API"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response({"message": "This is the post Student API"}, status=status.HTTP_200_OK)

# 定義 api_views 字典來註冊 API 視圖
api_views = {
    'student': StudentAPIView.as_view()
}