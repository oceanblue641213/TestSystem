from django.contrib.auth import get_user_model
from Domain.Exceptions.Exceptions import ResourceNotFoundException

User = get_user_model()

class UserService:
    def get_profile(self, user):
        try:
            # 業務邏輯處理
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        except User.DoesNotExist:
            raise ResourceNotFoundException("User")