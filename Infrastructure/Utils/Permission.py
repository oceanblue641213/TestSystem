from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 讀取權限允許所有請求
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 寫入權限只允許物件擁有者
        return obj.owner == request.user