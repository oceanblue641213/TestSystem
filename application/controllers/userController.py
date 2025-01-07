import logging
from drf_spectacular.utils import extend_schema
from django.core.cache import cache
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from infrastructure.utils.authentication import JWTAuthentication
import domain.entities.user as User
from domain.dtos.loginDto import LoginDto as dto
from infrastructure.utils.response import ApiResponse

# logger = logging.getLogger('django')

class LoginAPIView(APIView):
    @api_view(['POST'])
    @permission_classes([AllowAny])
    # @authentication_classes([JWTAuthentication])
    # @permission_classes([IsAuthenticated])
    @extend_schema(request=dto, methods=['POST'])
    async def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            
            # 密碼需解密
            password = request.data['password']
            
            # 帳號密碼驗證
            # user = authenticate(username=username, password=password)
            
            # if user:
            #     try:
            #         # 登入成功，紀錄logging
            #         # logger.info(f'User {username} logged in successfully', extra={
            #         #     'user_id': user.id,
            #         #     'ip_address': self.get_client_ip(request)
            #         # })
                    
            #         # 更新最後登入時間
            #         user.last_login = timezone.now()
            #         user.save()
                    
            #         # 生成 JWT
            #         refresh = RefreshToken.for_user(user)
                    
            #         return Response({
            #             'refresh': str(refresh),
            #             'access': str(refresh.access_token),
            #             'user_info': {
            #                 'id': user.id,
            #                 'username': user.username,
            #                 'email': user.email,
            #             }
            #         })
                
            #     except Exception as e:
            #         # logger.error(f'Login error for user {username}: {str(e)}')
            #         return Response({
            #             'error': 'Internal server error'
            #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # else:
            #     # 登入失敗
            #     # logger.warning(f'Failed login attempt for username {username}', extra={
            #     #     'ip_address': self.get_client_ip(request)
            #     # })
                
            #     return Response({
            #         'error': 'Invalid credentials'
            #     }, status=status.HTTP_401_UNAUTHORIZED)
            return ApiResponse.success(data='登入成功')
    
        except Exception as e:
            # 異常處理
            # logger.error(f"登入異常: {e}")
            return ApiResponse.error(message='系統異常')
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


api_views = {
    'login': LoginAPIView.as_view()
}


# 緩存數據
# cache.set('user_1_data', user_data, timeout=3600)  # 緩存1小時

# 讀取緩存
# cached_data = cache.get('user_1_data')
# if cached_data is None:
#     # 如果緩存不存在，重新查詢並緩存
#     cached_data = fetch_user_data()
#     cache.set('user_1_data', cached_data, timeout=3600)