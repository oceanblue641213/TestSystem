import jwt
from pathlib import Path
from rest_framework import authentication
from rest_framework import exceptions

class JWTAuthentication(authentication.BaseAuthentication):
    def __init__(self):
        # 讀取公鑰
        root_path = Path(__file__).parent.parent
        data_folder = 'Security'
        file_name = 'public.pem'
        file_file = root_path / data_folder / file_name
        
        with open(file_file, 'r') as f:
            self.PUBLIC_KEY = f.read()

    def authenticate(self, request):
        # 從請求頭獲取 Token
        token = request.headers.get('Token')
        
        if not token:
            return None

        try:
            # 驗證 Token
            payload = jwt.decode(
                token, 
                self.PUBLIC_KEY, 
                algorithms=["RS256"]
            )
            
            # 將 payload 存儲到 request 中，供後續使用
            request.user_data = payload
            
            # DRF 要求返回 (user, auth) 元組
            return (payload, None)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

    def authenticate_header(self, request):
        return 'Token'
    
    def verify_refresh_token(self, token):
        try:
            payload = jwt.decode(
                token, 
                self.PUBLIC_KEY, 
                algorithms=["RS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return 'expired'
        except jwt.InvalidTokenError:
            return None