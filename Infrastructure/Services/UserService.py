from django.contrib.auth import get_user_model
from Domain.Exceptions.Exceptions import ResourceNotFoundException
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login

User = get_user_model()

class UserService:
    @classmethod
    def register_user(cls, username, password):
        # 自動處理密碼加密
        user = User.objects.create(
            username=username,
            password=make_password(password)
        )
        return user

    @classmethod
    def login_user(cls, username, password):
        # Django 內建驗證
        user = authenticate(username=username, password=password)
        return user
    
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