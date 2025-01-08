from ninja.security import HttpBearer
import jwt
from django.conf import settings

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            # 驗證 JWT token
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=["HS256"]
            )
            return payload
        except jwt.InvalidTokenError:
            return None