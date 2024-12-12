from django.db import connection
from rest_framework.response import Response
import Infrastructure.Commands.Student.StudentCommand as stuCmd 
import Domain.Dtos.StudentDto as stdDto
from Infrastructure.Utils.Decorator import auto_swagger_and_validate
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

class StudentAPIView(APIView):
    @extend_schema(request=stdDto.StudentSerializer, methods=['POST'])
    def post(self, request, *args, **kwargs):
        try:
            dto = stdDto.StudentDto(**request.data)
            stuCmd.StudentCommand.Create_Student(dto)
            return Response({"message": "Students created successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

# 定義 api_views 字典來註冊 API 視圖
api_views = {
    'student': StudentAPIView.as_view()
}